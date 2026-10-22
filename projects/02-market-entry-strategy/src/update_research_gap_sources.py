import csv
from pathlib import Path

PROJECT = Path("projects/02-market-entry-strategy")
SOURCE_FILE = PROJECT / "data/external/source_register.csv"

HEADERS = [
    "source_id",
    "country",
    "evidence_domain",
    "indicator",
    "claim_or_finding",
    "source_organization",
    "source_title",
    "source_tier",
    "publication_date",
    "observation_period",
    "geographic_coverage",
    "metric_definition",
    "unit",
    "source_location",
    "access_date",
    "evidence_quality",
    "limitations",
    "analytical_use",
    "verification_status",
]

NEW_SOURCES = [
    {
        "source_id": "SRC-EURO-POL-SKIN",
        "country": "Poland",
        "evidence_domain": "Consumer market and category demand",
        "indicator": "Broad skincare market value and growth",
        "claim_or_finding": "Publisher listing describes skincare category coverage and historical data; exact required figures are not exposed in the public summary.",
        "source_organization": "Euromonitor International",
        "source_title": "Skin Care in Poland",
        "source_tier": "Tier 2",
        "publication_date": "May 2024",
        "observation_period": "Public listing describes data through 2023",
        "geographic_coverage": "Poland",
        "metric_definition": "Skincare category; consult full report for exact definition",
        "unit": "Not available in public summary",
        "source_location": "https://www.marketresearch.com/Euromonitor-International-v746/Poland-Skin-Care-36996690/",
        "access_date": "2026-10-20",
        "evidence_quality": "Publisher listing reviewed",
        "limitations": "Does not expose the required 2024 value and 2019-2024 CAGR.",
        "analytical_use": "Research lead only; not a quantitative input to the current comparison.",
        "verification_status": "Open; exact figures and methodology not verified",
    },
    {
        "source_id": "SRC-RM-POL-BPC",
        "country": "Poland",
        "evidence_domain": "Consumer market and category demand",
        "indicator": "Skincare market value and growth",
        "claim_or_finding": "Report contents indicate skincare value and growth tables for 2019-2024; exact figures are not exposed in the public summary.",
        "source_organization": "Euromonitor International",
        "source_title": "Beauty and Personal Care in Poland",
        "source_tier": "Tier 2",
        "publication_date": "May 2025",
        "observation_period": "2019-2024 tables indicated in report contents",
        "geographic_coverage": "Poland",
        "metric_definition": "Skincare within beauty and personal care; full definition requires report access",
        "unit": "Not available in public summary",
        "source_location": "https://www.researchandmarkets.com/reports/2544884/beauty_and_personal_care_in_poland",
        "access_date": "2026-10-20",
        "evidence_quality": "Publisher listing and report contents reviewed",
        "limitations": "Required numeric tables are not publicly visible.",
        "analytical_use": "Potential route to comparable evidence if full tables become available.",
        "verification_status": "Open; exact figures and methodology not verified",
    },
    {
        "source_id": "SRC-EURO-SAU-SKIN",
        "country": "Saudi Arabia",
        "evidence_domain": "Consumer market and category demand",
        "indicator": "Broad skincare market value and growth",
        "claim_or_finding": "Publisher listing indicates skincare value and growth tables for 2019-2024; exact figures are not exposed in the public summary.",
        "source_organization": "Euromonitor International",
        "source_title": "Skin Care in Saudi Arabia",
        "source_tier": "Tier 2",
        "publication_date": "May 2025",
        "observation_period": "2019-2024 tables indicated in report contents",
        "geographic_coverage": "Saudi Arabia",
        "metric_definition": "Skincare category; consult full report for exact definition",
        "unit": "Not available in public summary",
        "source_location": "https://www.marketresearch.com/Euromonitor-International-v746/Skin-Care-Saudi-Arabia-41124346/",
        "access_date": "2026-10-20",
        "evidence_quality": "Publisher listing reviewed",
        "limitations": "Required numeric tables are not publicly visible.",
        "analytical_use": "Research lead only; not a quantitative input to the current comparison.",
        "verification_status": "Open; exact figures and methodology not verified",
    },
    {
        "source_id": "SRC-GD-SAU-FACIAL",
        "country": "Saudi Arabia",
        "evidence_domain": "Consumer market and category demand",
        "indicator": "Facial-care market value and CAGR",
        "claim_or_finding": "Public listing reports 2024 facial-care sales of SAR 2,014.45 million and 2019-2024 CAGR of 5.11%.",
        "source_organization": "GlobalData",
        "source_title": "Saudi Arabia Facial Care (Skincare) Market Size, Growth and Forecast Analytics, 2024-2029",
        "source_tier": "Tier 2",
        "publication_date": "2026-05-08",
        "observation_period": "2024 market value; 2019-2024 CAGR",
        "geographic_coverage": "Saudi Arabia",
        "metric_definition": "Facial care only; narrower than the project's broad-skincare definition",
        "unit": "SAR million; percent per year",
        "source_location": "https://www.marketresearch.com/GlobalData-v3648/Saudi-Arabia-Facial-Care-Skincare-46109148/",
        "access_date": "2026-10-20",
        "evidence_quality": "Publisher listing reviewed",
        "limitations": "Facial care is not equivalent to broad skincare; do not combine with the MarketLine series.",
        "analytical_use": "Separate facial-care evidence only, if a distinct comparison is later justified.",
        "verification_status": "Publisher summary checked; full methodology not reviewed",
    },
    {
        "source_id": "SRC-RM-CHL-BPC",
        "country": "Chile",
        "evidence_domain": "Consumer market and category demand",
        "indicator": "Skincare market value and growth",
        "claim_or_finding": "Publisher contents indicate skincare category tables for 2019-2024; exact figures are not exposed in the public summary.",
        "source_organization": "Euromonitor International",
        "source_title": "Beauty and Personal Care in Chile",
        "source_tier": "Tier 2",
        "publication_date": "Not confirmed",
        "observation_period": "2019-2024 tables indicated in report contents",
        "geographic_coverage": "Chile",
        "metric_definition": "Skincare within beauty and personal care; full definition requires report access",
        "unit": "Not available in public summary",
        "source_location": "https://www.researchandmarkets.com/reports/2646908/beauty_and_personal_care_in_chile",
        "access_date": "2026-10-20",
        "evidence_quality": "Publisher contents reviewed",
        "limitations": "Required numeric tables are not publicly visible.",
        "analytical_use": "Potential route to comparable evidence if full tables become available.",
        "verification_status": "Open; exact figures and methodology not verified",
    },
    {
        "source_id": "SRC-GD-CHL-FACIAL",
        "country": "Chile",
        "evidence_domain": "Consumer market and category demand",
        "indicator": "Facial-care market value and CAGR",
        "claim_or_finding": "Public listing reports 2024 facial-care sales of CLP 315,745.92 million and 2019-2024 CAGR of 8.24%.",
        "source_organization": "GlobalData",
        "source_title": "Chile Facial Care (Skincare) Market Size, Growth and Forecast Analytics, 2024-2029",
        "source_tier": "Tier 2",
        "publication_date": "2026-05-08",
        "observation_period": "2024 market value; 2019-2024 CAGR",
        "geographic_coverage": "Chile",
        "metric_definition": "Facial care only; narrower than the project's broad-skincare definition",
        "unit": "CLP million; percent per year",
        "source_location": "https://www.marketresearch.com/GlobalData-v3648/Chile-Facial-Care-Skincare-Size-46107928/",
        "access_date": "2026-10-20",
        "evidence_quality": "Publisher listing reviewed",
        "limitations": "Facial care is not equivalent to broad skincare; do not combine with the MarketLine series.",
        "analytical_use": "Separate facial-care evidence only, if a distinct comparison is later justified.",
        "verification_status": "Publisher summary checked; full methodology not reviewed",
    },
]


def main():
    with SOURCE_FILE.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        existing_headers = reader.fieldnames
        existing_rows = list(reader)

    if existing_headers != HEADERS:
        raise ValueError(
            f"Unexpected source-register schema.\n"
            f"Expected {len(HEADERS)} headers; found {len(existing_headers or [])}.\n"
            f"No changes made."
        )

    existing_ids = {row["source_id"] for row in existing_rows}
    additions = [row for row in NEW_SOURCES if row["source_id"] not in existing_ids]

    if not additions:
        print("No new records added; all six source IDs already exist.")
        return

    for row in additions:
        if set(row) != set(HEADERS):
            raise ValueError(f"Incorrect fields in {row['source_id']}")

    all_rows = existing_rows + additions
    all_ids = [row["source_id"] for row in all_rows]

    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Duplicate source IDs detected. No changes made.")

    with SOURCE_FILE.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(all_rows)

    print("PASS: source register updated")
    print("Records before:", len(existing_rows))
    print("Records added:", len(additions))
    print("Records after:", len(all_rows))
    print("Unique source IDs:", len(set(all_ids)))
    print("All records use the 19-column schema.")


if __name__ == "__main__":
    main()