"""Build a wide country-level macroeconomic comparison dataset."""

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "country_macro_summary_v2.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "market_macro_comparison.csv"
)

EXPECTED_COUNTRIES = {
    "AUS",  # Australia
    "CHL",  # Chile
    "IDN",  # Indonesia
    "JPN",  # Japan
    "KOR",  # South Korea
    "POL",  # Poland
    "SAU",  # Saudi Arabia
    "TUR",  # Turkey
}

INDICATORS = {
    "NY.GDP.MKTP.CD": "gdp_current_usd",
    "NY.GDP.MKTP.KD.ZG": "real_gdp_growth_pct",
    "NY.GDP.PCAP.CD": "gdp_per_capita_current_usd",
    "SP.POP.TOTL": "population",
    "SP.POP.GROW": "population_growth_pct",
    "FP.CPI.TOTL.ZG": "inflation_pct",
    "NY.GDP.PCAP.PP.CD": "gdp_per_capita_ppp",
}

REQUIRED_COLUMNS = {
    "country_code",
    "country",
    "world_bank_code",
    "latest_year",
    "latest_value",
    "unit",
}


def main():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Summary dataset not found: {INPUT_PATH}"
        )

    with INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Input CSV has no header.")

        missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                f"Input is missing columns: {sorted(missing_columns)}"
            )

        rows = list(reader)

    if not rows:
        raise ValueError("Input summary contains no rows.")

    grouped = {}

    for row in rows:
        country_code = row["country_code"].strip()
        indicator_code = row["world_bank_code"].strip()

        if indicator_code not in INDICATORS:
            raise ValueError(
                f"Unexpected indicator: {indicator_code}"
            )

        key = (country_code, indicator_code)

        if key in grouped:
            raise ValueError(
                f"Duplicate country-indicator summary: {key}"
            )

        try:
            latest_year = int(row["latest_year"])
            latest_value = float(row["latest_value"])
        except (ValueError, TypeError) as exc:
            raise ValueError(
                f"Invalid latest year or value for {key}"
            ) from exc

        if not row["unit"].strip():
            raise ValueError(f"Missing unit for {key}")

        grouped[key] = {
            "country_code": country_code,
            "country": row["country"].strip(),
            "indicator_code": indicator_code,
            "latest_year": latest_year,
            "latest_value": latest_value,
            "unit": row["unit"].strip(),
        }

    found_countries = {
        country_code for country_code, _ in grouped
    }

    if found_countries != EXPECTED_COUNTRIES:
        raise ValueError(
            "Country coverage mismatch. "
            f"Missing: {sorted(EXPECTED_COUNTRIES - found_countries)}; "
            f"Unexpected: {sorted(found_countries - EXPECTED_COUNTRIES)}"
        )

    expected_pairs = {
        (country_code, indicator_code)
        for country_code in EXPECTED_COUNTRIES
        for indicator_code in INDICATORS
    }

    found_pairs = set(grouped)

    if found_pairs != expected_pairs:
        raise ValueError(
            "Country-indicator coverage mismatch. "
            f"Missing combinations: {sorted(expected_pairs - found_pairs)}; "
            f"Unexpected combinations: {sorted(found_pairs - expected_pairs)}"
        )

    output_fields = ["country_code", "country"]

    for indicator_name in INDICATORS.values():
        output_fields.extend(
            [
                indicator_name,
                f"{indicator_name}_year",
                f"{indicator_name}_unit",
            ]
        )

    comparison_rows = []

    for country_code in sorted(EXPECTED_COUNTRIES):
        country_records = [
            grouped[(country_code, indicator_code)]
            for indicator_code in INDICATORS
        ]

        country_names = {
            record["country"] for record in country_records
        }

        if len(country_names) != 1:
            raise ValueError(
                f"Inconsistent country names for {country_code}"
            )

        output_row = {
            "country_code": country_code,
            "country": country_records[0]["country"],
        }

        for indicator_code, column_name in INDICATORS.items():
            record = grouped[(country_code, indicator_code)]

            output_row[column_name] = record["latest_value"]
            output_row[f"{column_name}_year"] = record["latest_year"]
            output_row[f"{column_name}_unit"] = record["unit"]

        comparison_rows.append(output_row)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=output_fields,
        )
        writer.writeheader()
        writer.writerows(comparison_rows)

    print("MARKET MACRO COMPARISON")
    print("=======================")
    print(f"Countries: {len(comparison_rows)}")
    print(f"Indicators per country: {len(INDICATORS)}")
    print(f"Expected indicator values: {len(comparison_rows) * len(INDICATORS)}")
    print(f"Missing country-indicator combinations: 0")
    print(f"Output: {OUTPUT_PATH}")

    print("\nCountry coverage:")
    for row in comparison_rows:
        print(f"{row['country_code']}: {row['country']}")

    print(
        "\nInterpretation note: this dataset is a descriptive "
        "macroeconomic comparison, not a market attractiveness ranking. "
        "Indicator values retain their observation years and units. "
        "Different units and scales must not be compared directly."
    )


if __name__ == "__main__":
    main()