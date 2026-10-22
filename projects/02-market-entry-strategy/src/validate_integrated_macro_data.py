
"""Validate the integrated seven-indicator macroeconomic dataset."""

import csv
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "world_bank_macro_observations_v2.csv"
)

DICTIONARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "external"
    / "macro_indicator_dictionary.csv"
)

REPORT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "macro_data_quality_report_v2.csv"
)

EXPECTED_COUNTRIES = {
    "POL", "SAU", "AUS", "JPN", "KOR", "IDN", "TUR", "CHL"
}
EXPECTED_YEARS = set(range(2020, 2026))

# Broad screening bounds: outside a bound means investigate, not reject.
PLAUSIBLE_RANGES = {
    "NY.GDP.MKTP.CD": (0, 1e14),
    "NY.GDP.PCAP.CD": (0, 1e7),
    "NY.GDP.PCAP.PP.CD": (0, 1e7),
    "NY.GDP.MKTP.KD.ZG": (-30, 30),
    "SP.POP.TOTL": (0, 2e9),
    "SP.POP.GROW": (-5, 10),
    "FP.CPI.TOTL.ZG": (-10, 200),
}


def add_check(checks, name, passed, details):
    checks.append({
        "check_name": name,
        "status": "PASS" if passed else "REVIEW",
        "details": details,
    })


def main():
    checks = []
    errors = []

    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Integrated dataset not found: {DATA_PATH}")
    if not DICTIONARY_PATH.exists():
        raise FileNotFoundError(f"Indicator dictionary not found: {DICTIONARY_PATH}")

    with DICTIONARY_PATH.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        dictionary = list(csv.DictReader(file))

    expected_indicators = {
        row["world_bank_code"].strip()
        for row in dictionary
        if row.get("world_bank_code", "").strip()
    }

    with DATA_PATH.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)
        required_fields = {
            "country_code", "country", "indicator_id", "indicator_name",
            "world_bank_code", "year", "value", "unit",
            "source_organization", "source_url",
            "extraction_timestamp_utc",
        }

        headers = set(reader.fieldnames or [])
        if not required_fields.issubset(headers):
            missing = sorted(required_fields - headers)
            raise ValueError(f"Dataset is missing columns: {missing}")

        rows = list(reader)

    add_check(
        checks,
        "Dataset readable",
        True,
        f"{len(rows)} rows read without CSV parsing errors.",
    )

    country_codes = {row["country_code"].strip() for row in rows}
    indicator_codes = {row["world_bank_code"].strip() for row in rows}
    years = set()
    keys = []
    null_values = []
    missing_metadata = []
    implausible = []
    invalid_rows = []

    for row in rows:
        code = row["country_code"].strip()
        indicator = row["world_bank_code"].strip()

        try:
            year = int(row["year"])
            years.add(year)
            value = float(row["value"])
        except (TypeError, ValueError):
            invalid_rows.append(
                f"{code}/{indicator}/{row.get('year', '')}: invalid year or value"
            )
            continue

        keys.append((code, indicator, year))

        if not row["value"].strip():
            null_values.append(f"{code}/{indicator}/{year}")
            continue

        for field in (
            "country", "indicator_id", "indicator_name", "unit",
            "source_organization", "source_url",
            "extraction_timestamp_utc",
        ):
            if not row.get(field, "").strip():
                missing_metadata.append(f"{code}/{indicator}/{year}:{field}")

        bounds = PLAUSIBLE_RANGES.get(indicator)
        if bounds and not (bounds[0] <= value <= bounds[1]):
            implausible.append(
                f"{code}/{indicator}/{year}={value}; expected broad range {bounds}"
            )

    duplicate_count = len(keys) - len(set(keys))
    expected_count = (
        len(EXPECTED_COUNTRIES)
        * len(expected_indicators)
        * len(EXPECTED_YEARS)
    )

    add_check(
        checks, "Country coverage",
        country_codes == EXPECTED_COUNTRIES,
        f"Found {len(country_codes)} countries; "
        f"missing={sorted(EXPECTED_COUNTRIES-country_codes)}; "
        f"unexpected={sorted(country_codes-EXPECTED_COUNTRIES)}.",
    )
    add_check(
        checks, "Indicator coverage",
        indicator_codes == expected_indicators,
        f"Found {len(indicator_codes)} indicators; "
        f"missing={sorted(expected_indicators-indicator_codes)}; "
        f"unexpected={sorted(indicator_codes-expected_indicators)}.",
    )
    add_check(
        checks, "Year coverage",
        years == EXPECTED_YEARS,
        f"Found years={sorted(years)}; "
        f"missing={sorted(EXPECTED_YEARS-years)}; "
        f"unexpected={sorted(years-EXPECTED_YEARS)}.",
    )
    add_check(
        checks, "Unique country-indicator-year keys",
        duplicate_count == 0,
        f"{duplicate_count} duplicate key(s).",
    )
    add_check(
        checks, "Expected observation count",
        len(rows) == expected_count,
        f"Expected {expected_count}; found {len(rows)}.",
    )
    add_check(
        checks, "Valid numeric observations",
        len(invalid_rows) == 0,
        f"{len(invalid_rows)} invalid row(s). Examples: {invalid_rows[:5]}",
    )
    add_check(
        checks, "Missing values",
        len(null_values) == 0,
        f"{len(null_values)} blank or missing value(s). "
        f"Examples: {null_values[:5]}",
    )
    add_check(
        checks, "Required metadata",
        len(missing_metadata) == 0,
        f"{len(missing_metadata)} missing metadata field(s). "
        f"Examples: {missing_metadata[:5]}",
    )
    add_check(
        checks, "Broad plausibility ranges",
        len(implausible) == 0,
        f"{len(implausible)} value(s) outside broad ranges. "
        f"Examples: {implausible[:5]}",
    )

    generated_at = datetime.now(timezone.utc).isoformat()
    with REPORT_PATH.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        fields = ["check_name", "status", "details", "report_timestamp_utc"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for check in checks:
            writer.writerow({
                **check,
                "report_timestamp_utc": generated_at,
            })

    print("INTEGRATED MACRO DATA QUALITY REVIEW")
    print("====================================")
    print(f"Dataset rows: {len(rows)}")
    print(f"Countries found: {len(country_codes)}")
    print(f"Indicators found: {len(indicator_codes)}")
    print(f"Years found: {sorted(years)}")
    print()

    for check in checks:
        print(f"[{check['status']}] {check['check_name']}")
        print(f"       {check['details']}")

    print(f"\nQuality report saved to: {REPORT_PATH}")

    if any(check["status"] != "PASS" for check in checks):
        raise SystemExit(
            "Review required: one or more validation checks need investigation."
        )


if __name__ == "__main__":
    main()
