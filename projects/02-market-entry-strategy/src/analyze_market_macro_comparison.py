"""Produce a descriptive review of candidate-market macroeconomic indicators."""

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "market_macro_comparison.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "market_macro_indicator_review.csv"
)

# Each entry maps an indicator to its column, interpretation, and unit.
INDICATORS = {
    "Economic scale — GDP": {
        "value": "gdp_current_usd",
        "year": "gdp_current_usd_year",
        "unit": "gdp_current_usd_unit",
        "description": "Larger values indicate a larger overall economy.",
    },
    "Population": {
        "value": "population",
        "year": "population_year",
        "unit": "population_unit",
        "description": "Larger values indicate a larger national population.",
    },
    "GDP per capita": {
        "value": "gdp_per_capita_current_usd",
        "year": "gdp_per_capita_current_usd_year",
        "unit": "gdp_per_capita_current_usd_unit",
        "description": "Average economic output per person in current US dollars.",
    },
    "GDP per capita — PPP": {
        "value": "gdp_per_capita_ppp",
        "year": "gdp_per_capita_ppp_year",
        "unit": "gdp_per_capita_ppp_unit",
        "description": (
            "GDP per person adjusted for differences in purchasing power."
        ),
    },
    "Real GDP growth": {
        "value": "real_gdp_growth_pct",
        "year": "real_gdp_growth_pct_year",
        "unit": "real_gdp_growth_pct_unit",
        "description": "Annual growth in inflation-adjusted economic output.",
    },
    "Inflation": {
        "value": "inflation_pct",
        "year": "inflation_pct_year",
        "unit": "inflation_pct_unit",
        "description": (
            "Annual consumer price inflation; high inflation can increase "
            "pricing uncertainty and operating costs."
        ),
    },
    "Population growth": {
        "value": "population_growth_pct",
        "year": "population_growth_pct_year",
        "unit": "population_growth_pct_unit",
        "description": "Annual population growth rate.",
    },
}


def load_comparison():
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Comparison dataset not found: {INPUT_PATH}"
        )

    with INPUT_PATH.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("Comparison dataset has no header.")

        required = {"country_code", "country"}

        for details in INDICATORS.values():
            required.update(
                {
                    details["value"],
                    details["year"],
                    details["unit"],
                }
            )

        missing = required - set(reader.fieldnames)

        if missing:
            raise ValueError(
                f"Comparison dataset is missing columns: {sorted(missing)}"
            )

        rows = list(reader)

    if len(rows) != 8:
        raise ValueError(
            f"Expected 8 candidate markets; found {len(rows)}."
        )

    country_codes = [row["country_code"] for row in rows]

    if len(country_codes) != len(set(country_codes)):
        raise ValueError("Duplicate country rows detected.")

    for row in rows:
        for label, details in INDICATORS.items():
            try:
                value = float(row[details["value"]])
                year = int(row[details["year"]])
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Invalid value or year for {row['country']}, {label}."
                ) from exc

            if not row[details["unit"]].strip():
                raise ValueError(
                    f"Missing unit for {row['country']}, {label}."
                )

            if year < 1900 or year > 2100:
                raise ValueError(
                    f"Implausible observation year for "
                    f"{row['country']}, {label}: {year}"
                )

    return rows


def build_review(rows):
    """Create a long-format review, preserving original units and years."""

    review_rows = []

    for row in rows:
        for label, details in INDICATORS.items():
            review_rows.append(
                {
                    "country_code": row["country_code"],
                    "country": row["country"],
                    "indicator": label,
                    "indicator_value": float(row[details["value"]]),
                    "unit": row[details["unit"]],
                    "observation_year": int(row[details["year"]]),
                    "interpretation_guidance": details["description"],
                }
            )

    return review_rows


def print_indicator_comparisons(rows):
    """Print each indicator in a readable order, without scoring markets."""

    print("\nMACROECONOMIC INDICATOR COMPARISON")
    print("=================================")

    for label, details in INDICATORS.items():
        # Inflation is shown from lowest to highest to make the range easy
        # to inspect. This does not mean that the lowest value is always best.
        ascending = label == "Inflation"

        ordered = sorted(
            rows,
            key=lambda row: float(row[details["value"]]),
            reverse=not ascending,
        )

        print(f"\n{label}")
        print("-" * len(label))
        print(details["description"])

        for row in ordered:
            value = float(row[details["value"]])
            year = row[details["year"]]
            unit = row[details["unit"]]

            print(
                f"{row['country']:<16} "
                f"{value:>18,.4f} "
                f"{unit} "
                f"({year})"
            )


def main():
    rows = load_comparison()
    review_rows = build_review(rows)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        fieldnames = [
            "country_code",
            "country",
            "indicator",
            "indicator_value",
            "unit",
            "observation_year",
            "interpretation_guidance",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(review_rows)

    print(f"Countries reviewed: {len(rows)}")
    print(f"Indicators reviewed: {len(INDICATORS)}")
    print(f"Country-indicator observations: {len(review_rows)}")
    print(f"Review dataset saved to: {OUTPUT_PATH}")

    print_indicator_comparisons(rows)

    print(
        "\nIMPORTANT INTERPRETATION NOTES"
        "\n- These are descriptive comparisons, not market-entry scores."
        "\n- GDP measures total economic scale, not Aurevia's addressable "
        "category demand."
        "\n- GDP per capita is not a direct measure of target-customer income."
        "\n- PPP values help compare purchasing power but do not replace "
        "market-specific price and affordability research."
        "\n- High GDP growth and population growth do not guarantee demand "
        "for Aurevia's products."
        "\n- Inflation should be interpreted alongside exchange rates, "
        "costs, pricing power, and economic conditions."
        "\n- Check source definitions and observation years before drawing "
        "investment conclusions."
    )


if __name__ == "__main__":
    main()