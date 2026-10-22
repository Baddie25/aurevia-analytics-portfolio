
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "processed" / "skincare_market_comparison.csv"
OUTPUT = ROOT / "data" / "processed" / "skincare_market_comparison_analysis.csv"

df = pd.read_csv(INPUT)

required = {
    "country_code",
    "country_name",
    "market_value_usd_m",
    "value_cagr_pct",
}
missing = required - set(df.columns)

if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

if df["country_code"].duplicated().any():
    raise ValueError("Duplicate country codes found")

if df[["market_value_usd_m", "value_cagr_pct"]].isna().any().any():
    raise ValueError("Missing market values or CAGR values")

df["market_value_rank"] = (
    df["market_value_usd_m"]
    .rank(method="min", ascending=False)
    .astype(int)
)

df["value_cagr_rank"] = (
    df["value_cagr_pct"]
    .rank(method="min", ascending=False)
    .astype(int)
)

df["value_growth_direction"] = df["value_cagr_pct"].apply(
    lambda x: "Positive" if x > 0 else ("Negative" if x < 0 else "Flat")
)

df["interpretation_limit"] = (
    "Descriptive only; source comparability and full report methodology "
    "not yet verified"
)

df = df.sort_values("market_value_rank")
df.to_csv(OUTPUT, index=False)

print(f"PASS: wrote {OUTPUT}")
print(
    df[
        [
            "country_name",
            "market_value_rank",
            "value_cagr_rank",
            "value_growth_direction",
        ]
    ].to_string(index=False)
)
print("No composite score or investment recommendation generated.")
