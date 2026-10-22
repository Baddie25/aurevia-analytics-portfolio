
"""Collect only the PPP-adjusted GDP-per-capita indicator."""

import csv
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DICTIONARY_PATH = (
    PROJECT_ROOT / "data" / "external" / "macro_indicator_dictionary.csv"
)

INDICATOR_CODE = "NY.GDP.PCAP.PP.CD"
START_YEAR = 2020
END_YEAR = 2025

COUNTRIES = {
    "POL": "Poland",
    "SAU": "Saudi Arabia",
    "AUS": "Australia",
    "JPN": "Japan",
    "KOR": "South Korea",
    "IDN": "Indonesia",
    "TUR": "Turkey",
    "CHL": "Chile",
}

BASE_URL = "https://api.worldbank.org/v2/country"


def fetch_json(url, attempts=3):
    request = Request(
        url,
        headers={"User-Agent": "Aurevia-Portfolio-Research/1.0"},
    )

    for attempt in range(1, attempts + 1):
        try:
            with urlopen(request, timeout=60) as response:
                raw = response.read()
            return raw, json.loads(raw.decode("utf-8"))
        except (
            HTTPError, URLError, TimeoutError, json.JSONDecodeError
        ) as exc:
            if attempt == attempts:
                raise RuntimeError(f"Request failed: {url}\n{exc}") from exc
            time.sleep(attempt * 2)


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    with DICTIONARY_PATH.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        dictionary = list(csv.DictReader(file))

    matches = [
        row for row in dictionary
        if row["world_bank_code"].strip() == INDICATOR_CODE
    ]

    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one dictionary entry for {INDICATOR_CODE}; "
            f"found {len(matches)}."
        )

    indicator = matches[0]
    country_codes = ";".join(COUNTRIES.keys())
    params = urlencode({
        "date": f"{START_YEAR}:{END_YEAR}",
        "format": "json",
        "per_page": 20000,
    })
    url = (
        f"{BASE_URL}/{country_codes}/indicator/{INDICATOR_CODE}?{params}"
    )

    raw_bytes, payload = fetch_json(url)

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError("Unexpected World Bank API response.")

    metadata = payload[0]
    observations = payload[1] or []

    raw_path = RAW_DIR / (
        f"world_bank_{INDICATOR_CODE}_{START_YEAR}_{END_YEAR}.json"
    )
    raw_path.write_bytes(raw_bytes)

    total_pages = int(metadata.get("pages", 1))
    for page_number in range(2, total_pages + 1):
        page_params = urlencode({
            "date": f"{START_YEAR}:{END_YEAR}",
            "format": "json",
            "per_page": 20000,
            "page": page_number,
        })
        page_url = (
            f"{BASE_URL}/{country_codes}/indicator/"
            f"{INDICATOR_CODE}?{page_params}"
        )
        page_bytes, page_payload = fetch_json(page_url)

        if not isinstance(page_payload, list) or len(page_payload) < 2:
            raise ValueError(f"Unexpected API page {page_number}.")

        page_path = RAW_DIR / (
            f"world_bank_{INDICATOR_CODE}_{START_YEAR}_{END_YEAR}"
            f"_page_{page_number}.json"
        )
        page_path.write_bytes(page_bytes)
        observations.extend(page_payload[1] or [])

    extraction_time = datetime.now(timezone.utc).isoformat()
    rows = []

    for observation in observations:
        code = observation.get("countryiso3code", "")
        year_text = observation.get("date")
        value = observation.get("value")

        if code not in COUNTRIES or not year_text:
            continue

        year = int(year_text)
        if not START_YEAR <= year <= END_YEAR:
            continue

        rows.append({
            "country_code": code,
            "country": COUNTRIES[code],
            "indicator_id": indicator["indicator_id"].strip(),
            "indicator_name": indicator["indicator_name"].strip(),
            "world_bank_code": INDICATOR_CODE,
            "year": year,
            "value": value,
            "unit": indicator["unit"].strip(),
            "source_organization": indicator["source_organization"].strip(),
            "source_url": url,
            "extraction_timestamp_utc": extraction_time,
        })

    keys = [(r["country_code"], r["year"]) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate country-year observations detected.")

    if len(rows) != len(COUNTRIES) * (END_YEAR - START_YEAR + 1):
        raise ValueError(
            f"Expected 48 country-year observations, found {len(rows)}. "
            "Inspect the API response before proceeding."
        )

    output_path = (
        PROCESSED_DIR / "world_bank_ppp_gdp_per_capita.csv"
    )
    fields = [
        "country_code", "country", "indicator_id", "indicator_name",
        "world_bank_code", "year", "value", "unit",
        "source_organization", "source_url", "extraction_timestamp_utc",
    ]

    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Indicator: {INDICATOR_CODE}")
    print(f"Countries: {len({r['country_code'] for r in rows})}")
    print(f"Observation rows: {len(rows)}")
    print(f"Years: {sorted({r['year'] for r in rows})}")
    print(f"Null values: {sum(r['value'] is None for r in rows)}")
    print(f"Duplicate country-year keys: {len(keys) - len(set(keys))}")
    print(f"Raw response: {raw_path}")
    print(f"Processed data: {output_path}")


if __name__ == "__main__":
    main()
