
"""Summarize World Bank macroeconomic observations by country and indicator."""

import csv
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "world_bank_macro_observations.csv"
)
OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "processed" / "country_macro_summary.csv"
)

# These indicators are rates: changes are best expressed in percentage points.
RATE_INDICATORS = {
    "NY.GDP.MKTP.KD.ZG",  # Real GDP growth
    "SP.POP.GROW",        # Population growth
    "FP.CPI.TOTL.ZG",      # Inflation
}

VALUE_FIELDS = [
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


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input dataset not found: {INPUT_PATH}")

    with INPUT_PATH.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)
        required = {
            "country_code", "country", "indicator_id",
            "indicator_name", "world_bank_code", "year", "value", "unit",
        }
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError("Input dataset is missing required columns.")
        rows = list(reader)

    grouped = defaultdict(list)

    for row in rows:
        value_text = row["value"].strip()
        if not value_text:
            continue

        try:
            value = float(value_text)
            year = int(row["year"])
        except ValueError as exc:
            raise ValueError(
                f"Invalid year or value for {row['country_code']} "
                f"{row['world_bank_code']} {row['year']}"
            ) from exc

        key = (row["country_code"], row["world_bank_code"])
        grouped[key].append({
            **row,
            "year_int": year,
            "value_num": value,
        })

    generated_at = datetime.now(timezone.utc).isoformat()
    summary_rows = []

    for (country_code, indicator_code), observations in sorted(grouped.items()):
        observations.sort(key=lambda item: item["year_int"])

        # Require no more than one value per year for this country/indicator.
        years = [item["year_int"] for item in observations]
        if len(years) != len(set(years)):
            raise ValueError(
                f"Duplicate years for {country_code} {indicator_code}"
            )

        baseline = next(
            (item for item in observations if item["year_int"] == 2020),
            None,
        )
        latest = observations[-1]

        baseline_value = baseline["value_num"] if baseline else None
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
                    (latest_value - baseline_value) / abs(baseline_value)
                ) * 100

        period_average = sum(
            item["value_num"] for item in observations
        ) / len(observations)

        summary_rows.append({
            "country_code": country_code,
            "country": latest["country"],
            "indicator_id": latest["indicator_id"],
            "indicator_name": latest["indicator_name"],
            "world_bank_code": indicator_code,
            "unit": latest["unit"],
            "baseline_year": 2020 if baseline else "",
            "baseline_value": baseline_value if baseline else "",
            "latest_year": latest["year_int"],
            "latest_value": latest_value,
            "absolute_change": (
                absolute_change if absolute_change is not None else ""
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
        })

    with OUTPUT_PATH.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=VALUE_FIELDS)
        writer.writeheader()
        writer.writerows(summary_rows)

    print("COUNTRY MACRO SUMMARY")
    print("=====================")
    print(f"Input observations: {len(rows)}")
    print(f"Country-indicator summaries: {len(summary_rows)}")
    print(f"Countries: {len({r['country_code'] for r in summary_rows})}")
    print(f"Indicators: {len({r['world_bank_code'] for r in summary_rows})}")
    print(f"Output: {OUTPUT_PATH}")

    print("\nLatest values by country and indicator:")
    for row in summary_rows:
        print(
            f"{row['country']:<16} "
            f"{row['world_bank_code']:<22} "
            f"{row['latest_year']}  "
            f"{float(row['latest_value']):,.4f} {row['unit']}"
        )

    print(
        "\nInterpretation note: rate changes are expressed in percentage "
        "points. Other percentage changes are calculated only when the "
        "2020 baseline exists and is non-zero. Period averages use available "
        "observations and should not be compared without checking coverage."
    )


if __name__ == "__main__":
    main()
