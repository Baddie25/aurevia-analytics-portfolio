
"""Quality review for Aurevia Project 2 World Bank macro data.

Reads the processed dataset and writes a separate quality report.
Does not modify raw API responses or the collected observations.
"""

import csv
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "world_bank_macro_observations.csv"
REPORT_PATH = PROJECT_ROOT / "data" / "processed" / "macro_data_quality_report.csv"

EXPECTED_COUNTRIES = {
    "POL", "SAU", "AUS", "JPN", "KOR", "IDN", "TUR", "CHL"
}
EXPECTED_INDICATORS = {
    "NY.GDP.MKTP.CD",
    "NY.GDP.PCAP.CD",
    "NY.GDP.MKTP.KD.ZG",
    "SP.POP.TOTL",
    "SP.POP.GROW",
    "FP.CPI.TOTL.ZG",
}
EXPECTED_YEARS = set(range(2020, 2026))

# Broad screening bounds. Exceeding a bound triggers review, not automatic rejection.
PLAUSIBLE_RANGES = {
    "NY.GDP.MKTP.CD": (0, 1e14),
    "NY.GDP.PCAP.CD": (0, 1e7),
    "NY.GDP.MKTP.KD.ZG": (-30, 30),
    "SP.POP.TOTL": (0, 2e9),
    "SP.POP.GROW": (-5, 10),
    "FP.CPI.TOTL.ZG": (-10, 200),
}


def add_check(checks, check_name, status, details):
    checks.append({
        "check_name": check_name,
        "status": status,
        "details": details,
    })


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    with DATA_PATH.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)
        required_fields = {
            "country_code", "country", "indicator_id",
            "indicator_name", "world_bank_code", "year", "value",
            "unit", "source_organization", "source_url",
            "extraction_timestamp_utc",
        }

        if not reader.fieldnames or not required_fields.issubset(reader.fieldnames):
            raise ValueError("Dataset is missing one or more required columns.")

        rows = list(reader)

    checks = []
    observations = []
    parse_errors = []

    for line_number, row in enumerate(rows, start=2):
        try:
            year = int(row["year"])
        except (TypeError, ValueError):
            parse_errors.append(f"Line {line_number}: invalid year")
            continue

        raw_value = row["value"].strip()
        value = None

        if raw_value:
            try:
                value = float(raw_value)
            except ValueError:
                parse_errors.append(
                    f"Line {line_number}: non-numeric value {raw_value!r}"
                )

        observations.append({
            **row,
            "year_int": year,
            "value_num": value,
            "line_number": line_number,
        })

    add_check(
        checks, "Dataset readable",
        "PASS" if not parse_errors else "FAIL",
        f"{len(rows)} rows read; {len(parse_errors)} parsing error(s)."
        + (f" Examples: {parse_errors[:5]}" if parse_errors else ""),
    )

    country_codes = {r["country_code"] for r in observations}
    indicator_codes = {r["world_bank_code"] for r in observations}
    years = {r["year_int"] for r in observations}

    add_check(
        checks, "Country coverage",
        "PASS" if country_codes == EXPECTED_COUNTRIES else "REVIEW",
        f"Found {len(country_codes)} countries; "
        f"missing={sorted(EXPECTED_COUNTRIES - country_codes)}; "
        f"unexpected={sorted(country_codes - EXPECTED_COUNTRIES)}.",
    )

    add_check(
        checks, "Indicator coverage",
        "PASS" if indicator_codes == EXPECTED_INDICATORS else "REVIEW",
        f"Found {len(indicator_codes)} indicators; "
        f"missing={sorted(EXPECTED_INDICATORS - indicator_codes)}; "
        f"unexpected={sorted(indicator_codes - EXPECTED_INDICATORS)}.",
    )

    add_check(
        checks, "Year coverage",
        "PASS" if years == EXPECTED_YEARS else "REVIEW",
        f"Found years={sorted(years)}; "
        f"missing={sorted(EXPECTED_YEARS - years)}; "
        f"unexpected={sorted(years - EXPECTED_YEARS)}.",
    )

    keys = [
        (r["country_code"], r["world_bank_code"], r["year_int"])
        for r in observations
    ]
    duplicate_keys = [
        key for key, count in Counter(keys).items() if count > 1
    ]

    add_check(
        checks, "Unique country-indicator-year keys",
        "PASS" if not duplicate_keys else "FAIL",
        f"{len(duplicate_keys)} duplicate key(s). "
        f"Examples: {duplicate_keys[:5]}",
    )

    expected_count = (
        len(EXPECTED_COUNTRIES)
        * len(EXPECTED_INDICATORS)
        * len(EXPECTED_YEARS)
    )

    add_check(
        checks, "Expected observation count",
        "PASS" if len(observations) == expected_count else "REVIEW",
        f"Expected {expected_count}; found {len(observations)}.",
    )

    null_values = [r for r in observations if r["value_num"] is None]
    add_check(
        checks, "Missing values",
        "PASS" if not null_values else "REVIEW",
        f"{len(null_values)} observation(s) have blank values. "
        "Review these rather than replacing them with zero.",
    )

    missing_metadata = [
        r for r in observations
        if not r["country"].strip()
        or not r["indicator_name"].strip()
        or not r["unit"].strip()
        or not r["source_organization"].strip()
        or not r["source_url"].strip()
    ]
    add_check(
        checks, "Required observation metadata",
        "PASS" if not missing_metadata else "REVIEW",
        f"{len(missing_metadata)} observation(s) have missing descriptive metadata.",
    )

    # Check for implausible values using deliberately broad screening bounds.
    range_flags = []
    for r in observations:
        value = r["value_num"]
        code = r["world_bank_code"]

        if value is None or code not in PLAUSIBLE_RANGES:
            continue

        low, high = PLAUSIBLE_RANGES[code]
        if not low < value < high:
            range_flags.append(
                f"{r['country_code']} {code} {r['year_int']}: {value}"
            )

    add_check(
        checks, "Broad plausibility bounds",
        "PASS" if not range_flags else "REVIEW",
        f"{len(range_flags)} value(s) outside broad review bounds. "
        f"Examples: {range_flags[:8]}",
    )

    # Check that every expected combination is represented.
    observed_key_set = set(keys)
    missing_combinations = [
        (country, indicator, year)
        for country in sorted(EXPECTED_COUNTRIES)
        for indicator in sorted(EXPECTED_INDICATORS)
        for year in sorted(EXPECTED_YEARS)
        if (country, indicator, year) not in observed_key_set
    ]

    add_check(
        checks, "Combination completeness",
        "PASS" if not missing_combinations else "REVIEW",
        f"{len(missing_combinations)} expected combination(s) absent. "
        f"Examples: {missing_combinations[:8]}",
    )

    # Report the latest available year for each country-indicator pair.
    grouped = defaultdict(list)
    for r in observations:
        grouped[(r["country_code"], r["world_bank_code"])].append(r)

    latest_years = []
    for (country, indicator), group in sorted(grouped.items()):
        years_with_values = [
            r["year_int"] for r in group if r["value_num"] is not None
        ]
        latest_years.append(
            f"{country} {indicator}: "
            f"{max(years_with_values) if years_with_values else 'no non-missing value'}"
        )

    latest_values = [
        r for r in observations
        if r["value_num"] is not None
        and r["year_int"] == max(
            (x["year_int"] for x in grouped[(r["country_code"], r["world_bank_code"])]
             if x["value_num"] is not None),
            default=-1,
        )
    ]

    add_check(
        checks, "Latest available observation years",
        "INFO",
        "Latest non-missing year by country and indicator: "
        + "; ".join(latest_years),
    )

    # Basic time-series review: flag zero or negative values where positive
    # economic quantities are expected, and implausibly large annual changes.
    trend_flags = []
    positive_indicators = {
        "NY.GDP.MKTP.CD", "NY.GDP.PCAP.CD", "SP.POP.TOTL"
    }

    for (country, indicator), group in sorted(grouped.items()):
        ordered = sorted(group, key=lambda r: r["year_int"])
        previous = None

        for r in ordered:
            value = r["value_num"]

            if value is None:
                previous = None
                continue

            if indicator in positive_indicators and value <= 0:
                trend_flags.append(
                    f"{country} {indicator} {r['year_int']}: "
                    f"non-positive value {value}"
                )

            if previous is not None and previous["value_num"] != 0:
                change = (
                    value / previous["value_num"] - 1
                ) * 100

                # Broad flags for further investigation, not automatic failures.
                if indicator in positive_indicators and abs(change) > 50:
                    trend_flags.append(
                        f"{country} {indicator}: {previous['year_int']} to "
                        f"{r['year_int']} changed {change:.1f}%"
                    )

            previous = r

    add_check(
        checks, "Time-series plausibility",
        "PASS" if not trend_flags else "REVIEW",
        f"{len(trend_flags)} item(s) require review. "
        f"Examples: {trend_flags[:10]}",
    )

    report_timestamp = datetime.now(timezone.utc).isoformat()
    with REPORT_PATH.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["check_name", "status", "details", "report_timestamp_utc"],
        )
        writer.writeheader()
        for check in checks:
            writer.writerow({
                **check,
                "report_timestamp_utc": report_timestamp,
            })

    print("\nMACRO DATA QUALITY REVIEW")
    print("=========================")
    print(f"Dataset rows: {len(rows)}")
    print(f"Countries found: {len(country_codes)}")
    print(f"Indicators found: {len(indicator_codes)}")
    print(f"Years found: {sorted(years)}")
    print()

    for check in checks:
        print(f"[{check['status']}] {check['check_name']}")
        print(f"  {check['details']}")

    print(f"\nQuality report saved to: {REPORT_PATH}")

    if any(check["status"] == "FAIL" for check in checks):
        raise SystemExit(
            "One or more critical quality checks failed. Review the report."
        )


if __name__ == "__main__":
    main()
