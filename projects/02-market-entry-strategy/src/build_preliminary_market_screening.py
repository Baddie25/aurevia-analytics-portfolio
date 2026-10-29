
"""Build a preliminary market-screening dataset for Project 2.

Combines macroeconomic indicators, skincare market estimates, and competitor
evidence. Produces a screening dataset and a research-gap register.

Run from the repository root:
    python projects/02-market-entry-strategy/src/build_preliminary_market_screening.py
"""

from __future__ import annotations

from pathlib import Path
import re

import pandas as pd


# ---------------------------------------------------------------------
# 1. Paths and configuration
# ---------------------------------------------------------------------

PROJECT = Path("projects/02-market-entry-strategy")
DATA = PROJECT / "data"
EXTERNAL = DATA / "external"
PROCESSED = DATA / "processed"

MACRO_FILE = PROCESSED / "market_macro_comparison.csv"
SKINCARE_FILE = PROCESSED / "skincare_market_comparison.csv"
COMPETITOR_FILE = EXTERNAL / "skincare_competitor_landscape_evidence.csv"
UNIVERSE_FILE = EXTERNAL / "market_universe.csv"

OUTPUT_FILE = PROCESSED / "preliminary_market_screening.csv"
GAPS_FILE = PROCESSED / "preliminary_market_evidence_gaps.csv"

MISSING_SKINCARE_STATUS = "Comparable skincare estimate missing"


# ---------------------------------------------------------------------
# 2. Input helpers
# ---------------------------------------------------------------------

def read_csv(path: Path) -> pd.DataFrame:
    """Read a CSV with UTF-8 BOM support and validate its headers."""
    if not path.exists():
        raise FileNotFoundError(
            f"Required input file not found: {path}"
        )

    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = df.columns.astype(str).str.strip()

    if df.columns.duplicated().any():
        duplicates = df.columns[
            df.columns.duplicated()
        ].tolist()
        raise ValueError(
            f"{path.name} has duplicate column names: {duplicates}"
        )

    return df


def require_columns(
    df: pd.DataFrame,
    required: set[str],
    filename: str,
) -> None:
    """Fail early with a clear message if required columns are absent."""
    missing = required - set(df.columns)

    if missing:
        raise ValueError(
            f"{filename} is missing required columns: "
            f"{sorted(missing)}"
        )


def normalize_text(value: object) -> str:
    """Normalize country names for matching."""
    if pd.isna(value):
        return ""

    value = str(value).strip().casefold()
    return re.sub(r"[^a-z0-9]+", "", value)


def normalize_country_columns(
    df: pd.DataFrame,
    filename: str,
) -> pd.DataFrame:
    """Standardize country_code and country_name across source schemas."""
    df = df.copy()

    # The macro file uses 'country'; skincare may use 'country_name'.
    if "country_name" not in df.columns and "country" in df.columns:
        df = df.rename(columns={"country": "country_name"})

    require_columns(
        df,
        {"country_code", "country_name"},
        filename,
    )

    df["country_code"] = (
        df["country_code"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    df["country_name"] = (
        df["country_name"]
        .astype("string")
        .str.strip()
    )

    # Treat empty strings as missing values.
    df["country_code"] = df["country_code"].replace("", pd.NA)
    df["country_name"] = df["country_name"].replace("", pd.NA)

    return df


def require_unique_country_codes(
    df: pd.DataFrame,
    filename: str,
) -> None:
    """Prevent ambiguous country-level joins."""
    codes = df["country_code"]

    duplicated = (
        codes.notna()
        & codes.duplicated(keep=False)
    )

    if duplicated.any():
        values = sorted(
            codes.loc[duplicated].dropna().unique().tolist()
        )

        raise ValueError(
            f"{filename} has duplicate country codes: {values}. "
            "Resolve duplicates before screening."
        )


def load_universe_codes(
    macro: pd.DataFrame,
) -> set[str] | None:
    """Read candidate codes or map universe country names through macro data.

    The current market_universe.csv uses a 'country' column and does
    not include ISO country codes. In that case, country names are matched
    to the canonical names in market_macro_comparison.csv.
    """
    if not UNIVERSE_FILE.exists():
        print(
            f"WARNING: {UNIVERSE_FILE} not found; "
            "skipping universe comparison."
        )
        return None

    universe = read_csv(UNIVERSE_FILE)

    code_column = next(
        (
            col
            for col in ("country_code", "iso3", "iso3_code")
            if col in universe.columns
        ),
        None,
    )

    # Preferred route: use explicit country codes if available.
    if code_column:
        codes = (
            universe[code_column]
            .dropna()
            .astype(str)
            .str.strip()
            .str.upper()
        )

        codes = codes[codes.ne("")]

        if codes.duplicated().any():
            duplicates = sorted(
                codes[codes.duplicated(keep=False)].unique().tolist()
            )
            raise ValueError(
                f"{UNIVERSE_FILE.name} contains duplicate country codes: "
                f"{duplicates}"
            )

        return set(codes)

    # Fallback: the current universe file uses country names.
    name_column = next(
        (
            col
            for col in (
                "country_name",
                "country",
                "market",
                "country_or_market",
            )
            if col in universe.columns
        ),
        None,
    )

    if name_column is None:
        print(
            f"WARNING: {UNIVERSE_FILE.name} has no recognized country-code "
            "or country-name column; skipping universe comparison."
        )
        return None

    name_to_code = {
        normalize_text(row["country_name"]):
            str(row["country_code"]).strip().upper()
        for _, row in macro.dropna(
            subset=["country_name", "country_code"]
        ).iterrows()
    }

    names = (
        universe[name_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    mapped: dict[str, str] = {}
    unmatched: list[str] = []

    for name in names:
        key = normalize_text(name)

        if not key:
            continue

        if key in name_to_code:
            mapped[name] = name_to_code[key]
        else:
            unmatched.append(name)

    if unmatched:
        raise ValueError(
            f"Could not match these {UNIVERSE_FILE.name} country names "
            f"to {MACRO_FILE.name}: {sorted(set(unmatched))}. "
            "Align the names or add explicit ISO3 codes to the universe file."
        )

    codes = set(mapped.values())

    if not codes:
        raise ValueError(
            f"No usable candidate countries found in {UNIVERSE_FILE}."
        )

    return codes


# ---------------------------------------------------------------------
# 3. Build screening dataset
# ---------------------------------------------------------------------

def main() -> None:
    """Validate inputs, merge evidence, identify gaps, and save outputs."""
    PROCESSED.mkdir(parents=True, exist_ok=True)

    # Load and normalize the source datasets.
    macro = normalize_country_columns(
        read_csv(MACRO_FILE),
        MACRO_FILE.name,
    )

    skincare = normalize_country_columns(
        read_csv(SKINCARE_FILE),
        SKINCARE_FILE.name,
    )

    competitors = read_csv(COMPETITOR_FILE)

    # Validate the minimum schemas required by downstream operations.
    require_columns(
        macro,
        {"country_code", "country_name"},
        MACRO_FILE.name,
    )

    require_columns(
        skincare,
        {
            "country_code",
            "country_name",
            "market_value_usd_m",
            "value_cagr_pct",
            "market_value_period",
            "cagr_period",
            "evidence_status",
        },
        SKINCARE_FILE.name,
    )

    require_columns(
        competitors,
        {
            "evidence_id",
            "country_code",
            "company_or_brand",
            "observation_type",
            "metric_value",
            "unit",
            "verification_status",
        },
        COMPETITOR_FILE.name,
    )

    # Normalize identifiers consistently across all inputs.
    competitors["country_code"] = (
        competitors["country_code"]
        .astype("string")
        .str.strip()
        .str.upper()
    )

    competitors["country_code"] = (
        competitors["country_code"].replace("", pd.NA)
    )

    # Prevent ambiguous country-level joins.
    require_unique_country_codes(macro, MACRO_FILE.name)
    require_unique_country_codes(skincare, SKINCARE_FILE.name)

    # Macro data defines the canonical set of candidate markets.
    macro_codes = set(
        macro["country_code"].dropna().astype(str)
    )

    universe_codes = load_universe_codes(macro)

    if universe_codes is not None:
        missing_macro = universe_codes - macro_codes
        unexpected_macro = macro_codes - universe_codes

        if missing_macro or unexpected_macro:
            raise ValueError(
                "Macro country coverage does not match the market universe. "
                f"Missing macro countries: {sorted(missing_macro)}; "
                f"unexpected macro countries: {sorted(unexpected_macro)}."
            )

    # Convert market values to numbers. Invalid values become missing and
    # are explicitly flagged as evidence gaps instead of crashing later.
    for col in ("market_value_usd_m", "value_cagr_pct"):
        skincare[col] = pd.to_numeric(
            skincare[col],
            errors="coerce",
        )

    # Merge one row per country. Macro supplies canonical country names.
    skincare_for_merge = skincare.drop(
        columns=["country_name"],
        errors="ignore",
    )

    screening = macro.merge(
        skincare_for_merge,
        on="country_code",
        how="left",
        validate="one_to_one",
        indicator="_skincare_merge",
    )

    screening["country_name"] = screening["country_name"].fillna(
        screening["country_code"]
    )

    # Preserve the source evidence status where available.
    source_status = screening.get(
        "evidence_status",
        pd.Series(pd.NA, index=screening.index),
    )

    screening["skincare_market_evidence_status"] = (
        source_status.astype("string").str.strip()
    )

    screening["skincare_market_evidence_status"] = (
        screening["skincare_market_evidence_status"].replace("", pd.NA)
    )

    # A market-size estimate is missing if no skincare row matched or the
    # market value is missing. Do not infer an estimate from other fields.
    missing_market = (
        screening["_skincare_merge"].ne("both")
        | screening["market_value_usd_m"].isna()
    )

    screening.loc[
        missing_market,
        "skincare_market_evidence_status",
    ] = MISSING_SKINCARE_STATUS

    screening["skincare_market_evidence_status"] = (
        screening["skincare_market_evidence_status"].fillna(
            "Review required"
        )
    )

    # Aggregate competitor evidence before joining, preventing duplicate
    # observations from multiplying country-level screening rows.
    valid_competitors = competitors.loc[
        competitors["country_code"].notna()
    ].copy()

    if valid_competitors.empty:
        competitor_summary = pd.DataFrame(
            columns=[
                "country_code",
                "competitor_evidence_count",
                "competitor_brand_count",
                "competitor_observation_count",
            ]
        )
    else:
        competitor_summary = (
            valid_competitors
            .groupby("country_code", dropna=True)
            .agg(
                competitor_evidence_count=("evidence_id", "nunique"),
                competitor_brand_count=("company_or_brand", "nunique"),
                competitor_observation_count=("observation_type", "count"),
            )
            .reset_index()
        )

    screening = screening.merge(
        competitor_summary,
        on="country_code",
        how="left",
        validate="one_to_one",
    )

    count_columns = [
        "competitor_evidence_count",
        "competitor_brand_count",
        "competitor_observation_count",
    ]

    screening[count_columns] = (
        screening[count_columns]
        .fillna(0)
        .astype(int)
    )

    screening["competitor_evidence_status"] = (
        screening["competitor_evidence_count"]
        .gt(0)
        .map({
            True: "Evidence available",
            False: "Evidence gap",
        })
    )

    # Keep screening decisions transparent. Do not invent a composite score.
    screening["screening_evidence_status"] = "Review required"

    screening.loc[
        ~missing_market,
        "screening_evidence_status",
    ] = "Market estimate available"

    # Remove internal merge diagnostics from the deliverable.
    screening = screening.drop(
        columns=["_skincare_merge"],
        errors="ignore",
    )

    # -----------------------------------------------------------------
    # 4. Create the research-gap register
    # -----------------------------------------------------------------

    skincare_gaps = screening.loc[
        screening["skincare_market_evidence_status"].eq(
            MISSING_SKINCARE_STATUS
        ),
        ["country_code", "country_name"],
    ].copy()

    skincare_gaps["gap_type"] = "Skincare market-size evidence"

    skincare_gaps["missing_evidence"] = (
        "Comparable skincare market estimate or documented period"
    )

    skincare_gaps["next_research_action"] = (
        "Find a credible country-level estimate, record its source and "
        "period, and verify comparability before updating the screening."
    )

    competitor_gaps = screening.loc[
        screening["competitor_evidence_count"].eq(0),
        ["country_code", "country_name"],
    ].copy()

    competitor_gaps["gap_type"] = "Competitor evidence"

    competitor_gaps["missing_evidence"] = (
        "Competitor landscape observations recorded in the evidence register"
    )

    competitor_gaps["next_research_action"] = (
        "Research relevant brands and market presence; record sources "
        "and verification status for each observation."
    )

    gaps = pd.concat(
        [skincare_gaps, competitor_gaps],
        ignore_index=True,
    )

    if not gaps.empty:
        gaps = (
            gaps.drop_duplicates(
                subset=["country_code", "gap_type"]
            )
            .sort_values(
                ["country_code", "gap_type"],
                kind="stable",
            )
        )

    # -----------------------------------------------------------------
    # 5. Final integrity checks and save outputs
    # -----------------------------------------------------------------

    if screening["country_code"].isna().any():
        raise ValueError(
            "Screening output contains missing country codes."
        )

    if screening["country_code"].duplicated().any():
        raise ValueError(
            "Screening output contains duplicate country codes."
        )

    screening.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    gaps.to_csv(
        GAPS_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print(f"Screening dataset: {OUTPUT_FILE}")
    print(f"Evidence gaps: {GAPS_FILE}")
    print(f"Candidate markets: {len(screening)}")

    print(
        "Markets with skincare evidence gaps:",
        int(
            screening["skincare_market_evidence_status"]
            .eq(MISSING_SKINCARE_STATUS)
            .sum()
        ),
    )

    print(
        "Markets with no competitor evidence:",
        int(
            screening["competitor_evidence_count"]
            .eq(0)
            .sum()
        ),
    )

    print(f"Research-gap records: {len(gaps)}")


if __name__ == "__main__":
    main()
