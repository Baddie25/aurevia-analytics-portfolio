
"""Collect World Bank macroeconomic indicators for Aurevia Project 2.

Original API responses are preserved under data/raw/.
A standardized long-format dataset is written to data/processed/.
"""

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

START_YEAR = 2020
END_YEAR = 2025
BASE_URL = "https://api.worldbank.org/v2/country"

# ISO 3-letter country codes.
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

OUTPUT_FIELDS = [
    "country_code",
    "country",
    "indicator_id",
    "indicator_name",
    "world_bank_code",
    "year",
    "value",
    "unit",
    "source_organization",
    "source_url",
    "extraction_timestamp_utc",
]


def read_indicator_dictionary():
    """Load and validate the approved indicator dictionary."""
    if not DICTIONARY_PATH.exists():
        raise FileNotFoundError(
            f"Indicator dictionary not found: {DICTIONARY_PATH}"
        )

    with DICTIONARY_PATH.open(
        "r", newline="", encoding="utf-8-sig"
    ) as file:
        reader = csv.DictReader(file)
        required = {
            "indicator_id",
            "indicator_name",
            "world_bank_code",
            "unit",
            "source_organization",
            "source_url",
        }

        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            raise ValueError(
                "The indicator dictionary is missing required columns."
            )

        indicators = list(reader)

    if not indicators:
        raise ValueError("The indicator dictionary contains no indicators.")

    codes = [row["world_bank_code"].strip() for row in indicators]
    if any(not code for code in codes):
        raise ValueError("An indicator has a blank World Bank code.")

    if len(codes) != len(set(codes)):
        raise ValueError("Duplicate World Bank indicator codes found.")

    return indicators


def fetch_json(url, attempts=3):
    """Fetch a JSON API response with limited retries."""
    request = Request(
        url,
        headers={"User-Agent": "Aurevia-Portfolio-Research/1.0"},
    )

    for attempt in range(1, attempts + 1):
        try:
            with urlopen(request, timeout=60) as response:
                raw_bytes = response.read()

            payload = json.loads(raw_bytes.decode("utf-8"))
            return raw_bytes, payload

        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            if attempt == attempts:
                raise RuntimeError(
                    f"API request failed after {attempts} attempts: {url}\n"
                    f"Error: {exc}"
                ) from exc
            time.sleep(attempt * 2)

    raise RuntimeError(f"Unable to retrieve URL: {url}")


def collect_indicator(indicator, extraction_timestamp):
    """Retrieve and preserve one indicator for all candidate countries."""
    indicator_code = indicator["world_bank_code"].strip()
    country_codes = ";".join(COUNTRIES.keys())

    params = urlencode(
        {
            "date": f"{START_YEAR}:{END_YEAR}",
            "format": "json",
            "per_page": 20000,
        }
    )
    url = (
        f"{BASE_URL}/{country_codes}/indicator/{indicator_code}?{params}"
    )

    raw_bytes, payload = fetch_json(url)

    # Preserve the original response bytes without transforming the JSON.
    raw_path = RAW_DIR / f"world_bank_{indicator_code}_{START_YEAR}_{END_YEAR}.json"
    raw_path.write_bytes(raw_bytes)

    if not isinstance(payload, list) or len(payload) < 2:
        raise ValueError(
            f"Unexpected API response for indicator {indicator_code}."
        )

    metadata = payload[0]
    observations = payload[1] or []

    # If pagination occurs, retrieve and preserve all additional pages.
    total_pages = int(metadata.get("pages", 1))
    for page_number in range(2, total_pages + 1):
        page_params = urlencode(
            {
                "date": f"{START_YEAR}:{END_YEAR}",
                "format": "json",
                "per_page": 20000,
                "page": page_number,
            }
        )
        page_url = (
            f"{BASE_URL}/{country_codes}/indicator/"
            f"{indicator_code}?{page_params}"
        )
        page_bytes, page_payload = fetch_json(page_url)

        page_path = RAW_DIR / (
            f"world_bank_{indicator_code}_{START_YEAR}_{END_YEAR}"
            f"_page_{page_number}.json"
        )
        page_path.write_bytes(page_bytes)

        if not isinstance(page_payload, list) or len(page_payload) < 2:
            raise ValueError(
                f"Unexpected page {page_number} for {indicator_code}."
            )

        observations.extend(page_payload[1] or [])

    rows = []
    for observation in observations:
        country_info = observation.get("country") or {}
        country_code = observation.get("countryiso3code", "")
        country_name = country_info.get("value", "")
        year = observation.get("date")
        value = observation.get("value")

        # Ignore any unexpected country or year outside our defined scope.
        if country_code not in COUNTRIES:
            continue
        if not year or not START_YEAR <= int(year) <= END_YEAR:
            continue

        rows.append(
            {
                "country_code": country_code,
                "country": COUNTRIES[country_code],
                "indicator_id": indicator["indicator_id"].strip(),
                "indicator_name": indicator["indicator_name"].strip(),
                "world_bank_code": indicator_code,
                "year": int(year),
                "value": value,
                "unit": indicator["unit"].strip(),
                "source_organization": indicator[
                    "source_organization"
                ].strip(),
                "source_url": url,
                "extraction_timestamp_utc": extraction_timestamp,
            }
        )

    print(
        f"{indicator_code}: {len(rows)} observations; "
        f"API reports {metadata.get('total', 'unknown')} records; "
        f"raw response saved to {raw_path.name}"
    )

    return rows


def validate_observations(rows, indicators):
    """Check keys, coverage and values without inventing missing data."""
    expected_indicators = {
        row["world_bank_code"].strip() for row in indicators
    }

    seen_keys = set()
    for row in rows:
        key = (
            row["country_code"],
            row["world_bank_code"],
            row["year"],
        )
        if key in seen_keys:
            raise ValueError(f"Duplicate country-indicator-year key: {key}")
        seen_keys.add(key)

        if row["value"] is not None:
            try:
                float(row["value"])
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Non-numeric value found for {key}: {row['value']}"
                ) from exc

    actual_indicators = {row["world_bank_code"] for row in rows}
    unexpected = actual_indicators - expected_indicators
    if unexpected:
        raise ValueError(f"Unexpected indicators returned: {unexpected}")

    expected_combinations = (
        len(COUNTRIES) * len(expected_indicators) *
        (END_YEAR - START_YEAR + 1)
    )
    observed_combinations = len(seen_keys)
    missing_combinations = expected_combinations - observed_combinations

    if missing_combinations < 0:
        raise ValueError("More observations than expected; investigate.")

    null_values = sum(1 for row in rows if row["value"] is None)

    print("\nValidation summary")
    print("------------------")
    print(f"Candidate countries: {len(COUNTRIES)}")
    print(f"Indicators in dictionary: {len(indicators)}")
    print(f"Expected country-indicator-year combinations: {expected_combinations}")
    print(f"Returned country-indicator-year combinations: {observed_combinations}")
    print(f"Combinations not returned: {missing_combinations}")
    print(f"Returned observations with null values: {null_values}")
    print("Duplicate keys: 0")
    print(
        "Note: combinations not returned and null values require review; "
        "they are not automatically errors or zeroes."
    )


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    indicators = read_indicator_dictionary()
    extraction_timestamp = datetime.now(timezone.utc).isoformat()

    all_rows = []
    failures = []

    print(f"Collection window: {START_YEAR}-{END_YEAR}")
    print(f"Candidate countries: {len(COUNTRIES)}")
    print(f"Indicators to collect: {len(indicators)}\n")

    for indicator in indicators:
        try:
            all_rows.extend(
                collect_indicator(indicator, extraction_timestamp)
            )
        except (RuntimeError, ValueError, OSError) as exc:
            failures.append(
                {
                    "indicator_id": indicator["indicator_id"],
                    "world_bank_code": indicator["world_bank_code"],
                    "error": str(exc),
                }
            )
            print(f"ERROR collecting {indicator['world_bank_code']}: {exc}")

    output_path = PROCESSED_DIR / "world_bank_macro_observations.csv"
    with output_path.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(all_rows)

    validate_observations(all_rows, indicators)

    manifest = {
        "source": "World Bank Indicators API",
        "api_base_url": "https://api.worldbank.org/v2/",
        "collection_window": {
            "start_year": START_YEAR,
            "end_year": END_YEAR,
        },
        "countries": COUNTRIES,
        "indicators": [
            {
                "indicator_id": row["indicator_id"],
                "indicator_name": row["indicator_name"],
                "world_bank_code": row["world_bank_code"],
                "source_url": row["source_url"],
            }
            for row in indicators
        ],
        "extraction_timestamp_utc": extraction_timestamp,
        "processed_file": str(output_path.relative_to(PROJECT_ROOT)),
        "returned_observation_rows": len(all_rows),
        "failures": failures,
        "notes": [
            "Null observations are retained as null, not replaced with zero.",
            "Observation year is preserved for each returned value.",
            "API responses are saved separately under data/raw/.",
            "Check failures and missing combinations before analytical use.",
        ],
    }

    manifest_path = RAW_DIR / "world_bank_collection_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"\nProcessed dataset: {output_path}")
    print(f"Collection manifest: {manifest_path}")

    if failures:
        raise SystemExit(
            f"Collection completed with {len(failures)} indicator failure(s). "
            "Review the errors before using the dataset."
        )


if __name__ == "__main__":
    main()
