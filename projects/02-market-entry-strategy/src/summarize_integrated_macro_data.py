"""Summarize integrated World Bank macroeconomic observations by country and indicator."""

import csv
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "world_bank_macro_observations_v2.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "country_macro_summary_v2.csv"
)

EXPECTED_INDICATORS = {
    "NY.GDP.MKTP.CD",       # GDP, current US dollars
    "NY.GDP.MKTP.KD.ZG",    # Real GDP growth
    "NY.GDP.PCAP.CD",       # GDP per capita, current US dollars
    "SP.POP.TOTL",          # Total population
    "SP.POP.GROW",          # Population growth
    "FP.CPI.TOTL.ZG",       # Consumer price inflation
    "NY.GDP.PCAP.PP.CD",    # GDP per capita, PPP, current international dollars
}

# These indicators are rates. Their changes are expressed in percentage points.
RATE_INDICATORS = {
    "NY.GDP.MKTP.KD.ZG",
    "SP.POP.GROW",
    "FP.CPI.TOTL.ZG",
}

REQUIRED_COLUMNS = {
    "country_code",
    "country",
    "indicator_id",
    "indicator_name",
    "world_bank_code",
    "year",
    "value",
    "unit",
}

OUTPUT_FIELDS = [
    "country_code",
    "country",
    "indicator_id",
    "indicator_name",
    "world_bank_code",
    "unit",
    "baseline_year",
    "baseline_value",
    "latest_year",
    "latest_value",
    "absolute_change",
    "percent_change",
    "change_percentage_points",
    "period_average",
    "observations_available",
    "period_start",
    "period_end",
    "summary_generated_utc",
]


def load_observations():
    """Load and validate the integrated macroeconomic dataset."""

    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input dataset not found: {INPUT_PATH}"
        )

    with INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Input dataset has no header row.")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                "Input dataset is missing required columns: "
                f"{sorted(missing_columns)}"
            )

        rows = list(reader)

    if not rows:
        raise ValueError("Input dataset contains no observations.")

    found_indicators = {
        row["world_bank_code"].strip()
        for row in rows
        if row["world_bank_code"].strip()
    }

    if found_indicators != EXPECTED_INDICATORS:
        missing = EXPECTED_INDICATORS - found_indicators
        unexpected = found_indicators - EXPECTED_INDICATORS

        raise ValueError(
            "Indicator coverage mismatch. "
            f"Missing: {sorted(missing)}; "
            f"Unexpected: {sorted(unexpected)}"
        )

    return rows


def prepare_groups(rows):
    """Convert observations to numeric values and group by country and indicator."""

    grouped = defaultdict(list)

    for row in rows:
        country_code = row["country_code"].strip()
        indicator_code = row["world_bank_code"].strip()
        year_text = row["year"].strip()
        value_text = row["value"].strip()

        if not country_code or not indicator_code:
            raise ValueError(
                "An observation has a missing country code or indicator code."
            )

        if not year_text:
            raise ValueError(
                f"Missing year for {country_code}, {indicator_code}."
            )

        if not value_text:
            raise ValueError(
                f"Missing value for {country_code}, "
                f"{indicator_code}, {year_text}."
            )

        try:
            year = int(year_text)
            value = float(value_text)
        except ValueError as exc:
            raise ValueError(
                f"Invalid year or value for {country_code}, "
                f"{indicator_code}, {year_text}: {value_text!r}"
            ) from exc

        key = (country_code, indicator_code)

        grouped[key].append(
            {
                **row,
                "country_code": country_code,
                "world_bank_code": indicator_code,
                "year_int": year,
                "value_num": value,
            }
        )

    return grouped


def build_summary(grouped):
    """Calculate baseline, latest, change, and period-average measures."""

    generated_at = datetime.now(timezone.utc).isoformat()
    summary_rows = []

    for (country_code, indicator_code), observations in sorted(
        grouped.items()
    ):
        observations.sort(key=lambda item: item["year_int"])

        years = [item["year_int"] for item in observations]

        if len(years) != len(set(years)):
            raise ValueError(
                f"Duplicate years found for {country_code}, "
                f"{indicator_code}."
            )

        baseline = next(
            (
                item
                for item in observations
                if item["year_int"] == 2020
            ),
            None,
        )

        latest = observations[-1]

        baseline_value = (
            baseline["value_num"] if baseline is not None else None
        )
        latest_value = latest["value_num"]

        absolute_change = None
        percent_change = None
        change_percentage_points = None

        if baseline_value is not None:
            absolute_change = latest_value - baseline_value

            if indicator_code in RATE_INDICATORS:
                change_percentage_points = absolute_change

            elif baseline_value != 0:
                percent_change = (
                    (latest_value - baseline_value)
                    / abs(baseline_value)
                ) * 100

        period_average = sum(
            item["value_num"] for item in observations
        ) / len(observations)

        summary_rows.append(
            {
                "country_code": country_code,
                "country": latest["country"],
                "indicator_id": latest["indicator_id"],
                "indicator_name": latest["indicator_name"],
                "world_bank_code": indicator_code,
                "unit": latest["unit"],
                "baseline_year": 2020 if baseline is not None else "",
                "baseline_value": (
                    baseline_value
                    if baseline_value is not None
                    else ""
                ),
                "latest_year": latest["year_int"],
                "latest_value": latest_value,
                "absolute_change": (
                    absolute_change
                    if absolute_change is not None
                    else ""
                ),
                "percent_change": (
                    percent_change
                    if percent_change is not None
                    else ""
                ),
                "change_percentage_points": (
                    change_percentage_points
                    if change_percentage_points is not None
                    else ""
                ),
                "period_average": period_average,
                "observations_available": len(observations),
                "period_start": years[0],
                "period_end": years[-1],
                "summary_generated_utc": generated_at,
            }
        )

    return summary_rows


def write_summary(summary_rows):
    """Write the summary dataset to CSV."""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=OUTPUT_FIELDS,
        )
        writer.writeheader()
        writer.writerows(summary_rows)


def main():
    """Run the complete summary workflow."""

    rows = load_observations()
    grouped = prepare_groups(rows)
    summary_rows = build_summary(grouped)

    countries = {
        row["country_code"] for row in summary_rows
    }
    indicators = {
        row["world_bank_code"] for row in summary_rows
    }
    unique_pairs = {
        (row["country_code"], row["world_bank_code"])
        for row in summary_rows
    }

    print("INTEGRATED COUNTRY MACRO SUMMARY")
    print("================================")
    print(f"Input observations: {len(rows)}")
    print(f"Country-indicator summaries: {len(summary_rows)}")
    print(f"Countries: {len(countries)}")
    print(f"Indicators: {len(indicators)}")
    print(f"Unique country-indicator pairs: {len(unique_pairs)}")

    if len(indicators) != 7:
        raise ValueError(
            f"Expected 7 indicators; found {len(indicators)}."
        )

    if len(countries) != 8:
        raise ValueError(
            f"Expected 8 countries; found {len(countries)}."
        )

    if len(summary_rows) != len(unique_pairs):
        raise ValueError(
            "Duplicate country-indicator summaries were detected."
        )

    expected_summary_rows = len(countries) * len(indicators)

    if len(summary_rows) != expected_summary_rows:
        raise ValueError(
            f"Expected {expected_summary_rows} summaries; "
            f"found {len(summary_rows)}."
        )

    write_summary(summary_rows)

    print(f"Output: {OUTPUT_PATH}")
    print("\nLatest values by country and indicator:")

    for row in summary_rows:
        print(
            f"{row['country']:<16} "
            f"{row['world_bank_code']:<22} "
            f"{row['latest_year']}  "
            f"{float(row['latest_value']):,.4f} "
            f"{row['unit']}"
        )

    print(
        "\nInterpretation notes:"
        "\n- Changes in GDP growth, population growth, and inflation "
        "are expressed in percentage points."
        "\n- Relative percentage changes are calculated only when "
        "the 2020 baseline exists and is non-zero."
        "\n- Period averages use available observations; check "
        "coverage before comparing countries."
        "\n- Latest observation years can differ by country and indicator."
        "\n- These are historical descriptive statistics, not forecasts."
    )


if __name__ == "__main__":
    main()