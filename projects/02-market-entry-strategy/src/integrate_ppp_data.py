"""Integrate PPP GDP-per-capita observations into a new macro dataset."""

import csv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "processed"

MAIN_FILE = DATA_DIR / "world_bank_macro_observations.csv"
PPP_FILE = DATA_DIR / "world_bank_ppp_gdp_per_capita.csv"
OUTPUT_FILE = DATA_DIR / "world_bank_macro_observations_v2.csv"

EXPECTED_COUNTRIES = 8
EXPECTED_YEARS = set(range(2020, 2026))
PPP_CODE = "NY.GDP.PCAP.PP.CD"


def read_csv(path):
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not reader.fieldnames:
            raise ValueError(f"Missing CSV headers: {path}")
        return reader.fieldnames, list(reader)


def main():
    main_fields, main_rows = read_csv(MAIN_FILE)
    ppp_fields, ppp_rows = read_csv(PPP_FILE)

    if main_fields != ppp_fields:
        raise ValueError(
            "CSV column headers differ. Do not integrate until reviewed.\n"
            f"Main: {main_fields}\nPPP: {ppp_fields}"
        )

    if any(row["world_bank_code"] == PPP_CODE for row in main_rows):
        raise ValueError(
            f"{PPP_CODE} already exists in the main dataset. "
            "Integration stopped to prevent duplicate observations."
        )

    expected_rows = EXPECTED_COUNTRIES * len(EXPECTED_YEARS)
    if len(ppp_rows) != expected_rows:
        raise ValueError(
            f"Expected {expected_rows} PPP rows; found {len(ppp_rows)}."
        )

    ppp_countries = {row["country_code"] for row in ppp_rows}
    ppp_years = {int(row["year"]) for row in ppp_rows}

    if len(ppp_countries) != EXPECTED_COUNTRIES:
        raise ValueError(
            f"Expected {EXPECTED_COUNTRIES} PPP countries; "
            f"found {len(ppp_countries)}."
        )

    if ppp_years != EXPECTED_YEARS:
        raise ValueError(f"Unexpected PPP years: {sorted(ppp_years)}")

    ppp_keys = [(row["country_code"], row["year"]) for row in ppp_rows]
    if len(ppp_keys) != len(set(ppp_keys)):
        raise ValueError("Duplicate PPP country-year keys detected.")

    main_keys = {
        (row["country_code"], row["world_bank_code"], row["year"])
        for row in main_rows
    }
    new_keys = [
        (row["country_code"], row["world_bank_code"], row["year"])
        for row in ppp_rows
    ]

    if any(key in main_keys for key in new_keys):
        raise ValueError(
            "Some PPP observation keys already exist in the main dataset."
        )

    combined_rows = main_rows + ppp_rows
    combined_keys = [
        (row["country_code"], row["world_bank_code"], row["year"])
        for row in combined_rows
    ]

    if len(combined_keys) != len(set(combined_keys)):
        raise ValueError("Duplicate country-indicator-year keys detected.")

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=main_fields)
        writer.writeheader()
        writer.writerows(combined_rows)

    print("PPP INTEGRATION SUMMARY")
    print("=======================")
    print(f"Original rows: {len(main_rows)}")
    print(f"PPP rows added: {len(ppp_rows)}")
    print(f"Integrated rows: {len(combined_rows)}")
    print(
        "Countries:",
        len({row["country_code"] for row in combined_rows}),
    )
    print(
        "Indicators:",
        len({row["world_bank_code"] for row in combined_rows}),
    )
    print(f"Duplicate country-indicator-year keys: 0")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()