
from pathlib import Path

import pandas as pd


# ============================================================
# Aurevia Group — Project 2: Market Entry Strategy
# Market Evidence Interpretation
#
# Purpose:
# Combine macroeconomic context and available broad-skincare
# evidence without creating an unsupported composite score,
# country ranking, or investment recommendation.
# ============================================================

PROJECT = Path("projects/02-market-entry-strategy")
DATA = PROJECT / "data" / "processed"
DOCS = PROJECT / "docs"

MACRO_FILE = DATA / "market_macro_comparison.csv"
SKINCARE_FILE = DATA / "skincare_market_comparison.csv"

OUTPUT_CSV = DATA / "market_evidence_interpretation.csv"
OUTPUT_MD = DOCS / "market-evidence-interpretation.md"


def validate_inputs(macro, skincare):
    """Validate schemas, expected coverage, and unique country keys."""

    required_macro = {
        "country_code",
        "country",
        "gdp_current_usd",
        "real_gdp_growth_pct",
        "gdp_per_capita_current_usd",
        "population",
        "population_growth_pct",
        "inflation_pct",
        "gdp_per_capita_ppp",
    }

    required_skincare = {
        "country_code",
        "country_name",
        "market_value_usd_m",
        "value_cagr_pct",
        "market_value_period",
        "cagr_period",
        "evidence_status",
    }

    missing_macro = required_macro - set(macro.columns)
    missing_skincare = required_skincare - set(skincare.columns)

    if missing_macro:
        raise ValueError(
            f"Macro dataset is missing columns: {sorted(missing_macro)}"
        )

    if missing_skincare:
        raise ValueError(
            "Skincare dataset is missing columns: "
            f"{sorted(missing_skincare)}"
        )

    if macro["country_code"].isna().any():
        raise ValueError("Macro dataset contains missing country codes.")

    if skincare["country_code"].isna().any():
        raise ValueError("Skincare dataset contains missing country codes.")

    if macro["country_code"].duplicated().any():
        raise ValueError("Macro dataset contains duplicate country codes.")

    if skincare["country_code"].duplicated().any():
        raise ValueError("Skincare dataset contains duplicate country codes.")

    if macro["country_code"].nunique() != 8:
        raise ValueError("Expected eight candidate markets in macro data.")

    if skincare["country_code"].nunique() != 5:
        raise ValueError("Expected five markets in the skincare comparison.")

    numeric_macro = [
        "gdp_current_usd",
        "real_gdp_growth_pct",
        "gdp_per_capita_current_usd",
        "population",
        "population_growth_pct",
        "inflation_pct",
        "gdp_per_capita_ppp",
    ]

    for column in numeric_macro:
        macro[column] = pd.to_numeric(macro[column], errors="raise")

    for column in ["market_value_usd_m", "value_cagr_pct"]:
        skincare[column] = pd.to_numeric(skincare[column], errors="raise")

    if macro[numeric_macro].isna().any().any():
        raise ValueError("Macro dataset contains missing required values.")

    if macro[numeric_macro].isin([float("inf"), float("-inf")]).any().any():
        raise ValueError("Macro dataset contains infinite numeric values.")

    if skincare[["market_value_usd_m", "value_cagr_pct"]].isna().any().any():
        raise ValueError("Skincare dataset contains missing market metrics.")

    if (skincare["market_value_usd_m"] < 0).any():
        raise ValueError("Skincare market value cannot be negative.")

    # Expected broad-skincare evidence gaps.
    expected_gaps = {"POL", "SAU", "CHL"}
    macro_codes = set(macro["country_code"])
    skincare_codes = set(skincare["country_code"])

    if not expected_gaps.issubset(macro_codes):
        raise ValueError(
            "Macro dataset does not contain all expected candidate markets."
        )

    unexpected_skincare_codes = skincare_codes - macro_codes
    if unexpected_skincare_codes:
        raise ValueError(
            "Skincare data contains countries outside the candidate "
            f"universe: {sorted(unexpected_skincare_codes)}"
        )

    if not skincare["market_value_period"].astype(str).str.fullmatch(
        r"\d{4}(\.0)?"
    ).all():
        raise ValueError("Unexpected skincare market-value period format.")


def format_macro_context(row):
    """Summarise macro indicators without implying category demand."""

    return (
        f"2025 GDP: US${row['gdp_current_usd'] / 1e9:,.1f}bn; "
        f"population: {row['population'] / 1e6:,.1f}m; "
        f"real GDP growth: {row['real_gdp_growth_pct']:.2f}%; "
        f"inflation: {row['inflation_pct']:.2f}%; "
        f"GDP per capita (PPP): "
        f"international ${row['gdp_per_capita_ppp']:,.0f}."
    )


def interpret_skincare_evidence(row):
    """Describe available category evidence or document its absence."""

    if not row["skincare_evidence_available"]:
        return (
            "Comparable broad-skincare market value and CAGR are "
            "unavailable in the current comparison. Do not infer category "
            "demand from macroeconomic indicators alone."
        )

    value = row["market_value_usd_m"]
    cagr = row["value_cagr_pct"]

    # Correctly display the market-value period as a year, not a float.
    market_value_year = int(float(row["market_value_period"]))
    cagr_period = str(row["cagr_period"])

    if cagr < 0:
        direction = "negative"
    elif cagr > 0:
        direction = "positive"
    else:
        direction = "flat"

    return (
        f"Reported {market_value_year} broad-skincare market value: "
        f"US${value:,.1f}m; reported {cagr_period} value CAGR: "
        f"{cagr:+.1f}% ({direction}). This is a descriptive "
        "publisher-summary estimate. Full methodology and cross-country "
        "comparability remain to be verified."
    )


def identify_next_action(row):
    """Set a research action without making an investment decision."""

    if not row["skincare_evidence_available"]:
        return (
            "Obtain comparable broad-skincare market value and historical "
            "CAGR, or document the gap if unavailable. Do not penalise the "
            "market simply because public evidence is incomplete."
        )

    if row["value_cagr_pct"] < 0:
        return (
            "Investigate the drivers of reported market-value decline. "
            "Seek evidence on sales volume, prices, product mix and "
            "currency treatment. The current data does not establish "
            "which factor explains the decline."
        )

    return (
        "Investigate whether reported category growth is supported by "
        "sales volume, pricing or product mix, then assess Aurevia's "
        "target segment, competitive position and feasible channels."
    )


def build_interpretation(macro, skincare):
    """Merge datasets and calculate separate descriptive indicators."""

    df = macro.merge(
        skincare,
        on="country_code",
        how="left",
        validate="one_to_one",
        suffixes=("_macro", "_skincare"),
    )

    # Country names in the macro dataset are the master labels.
    df["skincare_evidence_available"] = df["market_value_usd_m"].notna()

    # Separate descriptive ranks. These are NOT combined into a score.
    rank_definitions = {
        "gdp_scale_rank": ("gdp_current_usd", False),
        "population_rank": ("population", False),
        "real_gdp_growth_rank": ("real_gdp_growth_pct", False),
        "inflation_rank": ("inflation_pct", True),
        "gdp_per_capita_ppp_rank": ("gdp_per_capita_ppp", False),
    }

    for rank_name, (column, ascending) in rank_definitions.items():
        df[rank_name] = (
            df[column].rank(method="min", ascending=ascending).astype(int)
        )

    df["market_value_rank"] = df["market_value_usd_m"].rank(
        method="min", ascending=False
    ).astype("Int64")

    df["skincare_value_cagr_rank"] = df["value_cagr_pct"].rank(
        method="min", ascending=False
    ).astype("Int64")

    df["macro_context_2025"] = df.apply(format_macro_context, axis=1)
    df["skincare_evidence_interpretation"] = df.apply(
        interpret_skincare_evidence, axis=1
    )
    df["screening_implication"] = df.apply(identify_next_action, axis=1)

    df["interpretation_limit"] = (
        "No composite score or investment decision. GDP and population "
        "are contextual indicators, not category demand. GDP per capita "
        "and PPP are proxies, not direct measures of target-customer "
        "affordability. Skincare market-value growth does not establish "
        "volume growth or explain price, mix, inflation or exchange-rate "
        "effects. Publisher methodologies require further verification."
    )

    return df.sort_values("country_code").reset_index(drop=True)


def write_csv(df):
    """Write the structured interpretation dataset."""

    output_columns = [
        "country_code",
        "country",
        "gdp_current_usd",
        "gdp_scale_rank",
        "population",
        "population_rank",
        "real_gdp_growth_pct",
        "real_gdp_growth_rank",
        "inflation_pct",
        "inflation_rank",
        "gdp_per_capita_current_usd",
        "gdp_per_capita_ppp",
        "gdp_per_capita_ppp_rank",
        "market_value_usd_m",
        "market_value_rank",
        "value_cagr_pct",
        "skincare_value_cagr_rank",
        "market_value_period",
        "cagr_period",
        "evidence_status",
        "skincare_evidence_available",
        "macro_context_2025",
        "skincare_evidence_interpretation",
        "screening_implication",
        "interpretation_limit",
    ]

    df[output_columns].to_csv(OUTPUT_CSV, index=False)


def write_markdown(df):
    """Generate the written evidence review from the validated dataset."""

    lines = [
        "# Aurevia Group",
        "",
        "> **Data, Strategy, Decision Intelligence & Responsible AI Portfolio**",
        "",
        "---",
        "",
        "# Project 2 — Market Entry Strategy",
        "## Market Evidence Interpretation",
        "",
        "### Purpose",
        "",
        "This review combines the current macroeconomic comparison with "
        "the available broad-skincare market evidence. It supports market "
        "screening, not a final entry decision.",
        "",
        "### Evidence coverage",
        "",
        f"- Candidate markets in the macroeconomic dataset: {len(df)}.",
        f"- Markets with skincare figures in the current comparison: "
        f"{int(df['skincare_evidence_available'].sum())}.",
        f"- Markets without comparable skincare figures: "
        f"{int((~df['skincare_evidence_available']).sum())}.",
        "- Macro indicators describe economic context; they do not "
        "measure Aurevia's addressable category demand.",
        "",
        "### Time alignment and comparability",
        "",
        "- Macroeconomic context uses 2025 observations. Skincare market "
        "values refer to 2024, while historical value CAGR covers "
        "2019-2024. These indicators describe different periods and "
        "should not be interpreted as perfectly time-aligned.",
        "- The five skincare estimates are based on publisher summaries. "
        "Full report methodologies have not been reviewed, so category "
        "definitions, retail-value basis, exchange-rate treatment and "
        "cross-country comparability still require verification.",
        "- Market-value CAGR describes changes in reported market value, "
        "not necessarily changes in physical sales volume. The current "
        "dataset does not establish the contribution of price, volume, "
        "product mix, inflation or exchange rates.",
        "",
        "### Market-by-market interpretation",
        "",
    ]

    for _, row in df.iterrows():
        lines.extend(
            [
                f"### {row['country']}",
                "",
                f"- **Macroeconomic context:** {row['macro_context_2025']}",
                f"- **Skincare evidence:** "
                f"{row['skincare_evidence_interpretation']}",
                f"- **Next screening action:** {row['screening_implication']}",
                "",
            ]
        )

    lines.extend(
        [
            "### Cross-market conclusions",
            "",
            "1. Economic scale and population provide context, but do not "
            "establish skincare demand or Aurevia's likely market share.",
            "2. GDP per capita and PPP are broad affordability proxies; "
            "they do not measure the income or spending behaviour of "
            "Aurevia's target customers.",
            "3. Market value and value CAGR should be assessed separately. "
            "A large market can have declining value, while a smaller "
            "market can be growing.",
            "4. Value growth can reflect changes in volume, price, product "
            "mix, inflation and exchange rates. These are factors to "
            "investigate, not explanations established by the current data.",
            "5. Poland, Saudi Arabia and Chile remain evidence gaps in the "
            "broad-skincare comparison. Missing public evidence is not "
            "evidence of weak market attractiveness.",
            "6. The current publisher summaries have not been validated "
            "against the full report methodologies. Verify category "
            "definitions, retail-value basis, observation periods and "
            "currency treatment before relying on cross-country "
            "differences.",
            "",
            "### Decisions not yet supported",
            "",
            "- No composite country score or definitive market ranking.",
            "- No conclusion about Aurevia's addressable market, achievable "
            "market share, profitability or entry returns.",
            "- No final enter, delay or do-not-enter recommendation.",
            "",
            "### Next research priorities",
            "",
            "1. Resolve or explicitly retain the three broad-skincare "
            "evidence gaps.",
            "2. Verify category definitions and source methodology for "
            "the five existing market estimates.",
            "3. Investigate volume growth and price/mix effects, especially "
            "where reported value growth is negative.",
            "4. Map the category evidence to Aurevia's actual product "
            "categories and target customer segments.",
            "5. Research competitors, regulation, channels and local "
            "operating requirements before modelling entry economics.",
            "6. Use validated market, cost, investment and risk evidence "
            "before developing an investment decision.",
            "",
            "### Method note",
            "",
            "Indicator ranks in the accompanying CSV are separate "
            "descriptive comparisons. They are not combined into a score. "
            "The interpretation is based on the current project datasets; "
            "it does not replace source verification or investment analysis.",
            "",
        ]
    )

    OUTPUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main():
    macro = pd.read_csv(MACRO_FILE)
    skincare = pd.read_csv(SKINCARE_FILE)

    validate_inputs(macro, skincare)

    df = build_interpretation(macro, skincare)

    DOCS.mkdir(parents=True, exist_ok=True)

    write_csv(df)
    write_markdown(df)

    print("PASS: market evidence interpretation created")
    print("Candidate markets:", len(df))
    print(
        "Markets with skincare evidence:",
        int(df["skincare_evidence_available"].sum()),
    )
    print(
        "Markets without skincare evidence:",
        int((~df["skincare_evidence_available"]).sum()),
    )
    print("No composite score or investment decision generated.")
    print("CSV:", OUTPUT_CSV)
    print("Markdown:", OUTPUT_MD)


if __name__ == "__main__":
    main()
