from datetime import datetime, timezone
from pathlib import Path
from time import sleep, monotonic
from urllib.parse import urljoin
import json
import re

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl, ValidationError


BASE_URL = "https://books.toscrape.com/"
SCRAPER_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = SCRAPER_DIR / "cache"
OUTPUT_DIR = SCRAPER_DIR / "output"

USER_AGENT = (
    "FlyRankInternship-A9/1.0 "
    "(+https://github.com/Benzyma99/FlyRank-internship-)"
)

TIMEOUT = 10
REQUEST_DELAY = 0.5


class BookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: str | None
    source_page: HttpUrl
    fetched_at: datetime


def fetch_page(url: str, cache_file: Path) -> tuple[str, bool]:
    """Fetch a page or read it from cache."""

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if cache_file.exists():
        raw_content = cache_file.read_bytes()
        content = raw_content.decode("utf-8", errors="replace")

        print(f"CACHE HIT: {url} ({len(raw_content)} bytes)")
        return content, True

    attempts = 2

    for attempt in range(1, attempts + 1):
        try:
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=TIMEOUT,
            )

            status = response.status_code

            if status == 200:
                cache_file.write_bytes(response.content)

                print(
                    f"FETCH: {url} "
                    f"({len(response.content)} bytes)"
                )

                return response.text, False

            if status in {403, 404}:
                raise RuntimeError(
                    f"HTTP {status} — no retry for {url}"
                )

            if 500 <= status <= 599:
                if attempt < attempts:
                    print(
                        f"RETRY: HTTP {status} — "
                        f"{url}"
                    )
                    sleep(REQUEST_DELAY)
                    continue

                raise RuntimeError(
                    f"HTTP {status} after retry — {url}"
                )

            raise RuntimeError(
                f"HTTP {status} for {url}"
            )

        except requests.Timeout:
            if attempt < attempts:
                print(f"RETRY: timeout — {url}")
                sleep(REQUEST_DELAY)
                continue

            raise RuntimeError(
                f"Timeout after retry — {url}"
            )

        except requests.RequestException as exc:
            raise RuntimeError(
                f"Request failed: {exc}"
            ) from exc

    raise RuntimeError(f"Failed to fetch {url}")


def discover_books() -> dict[str, str]:
    """Discover book URLs from the first three catalogue pages."""

    current_url = BASE_URL
    catalogue_pages = 0
    book_urls = {}

    while current_url and catalogue_pages < 3:
        catalogue_pages += 1

        cache_file = CACHE_DIR / (
            f"catalogue-page-{catalogue_pages}.html"
        )

        html, _ = fetch_page(current_url, cache_file)

        soup = BeautifulSoup(html, "html.parser")

        for link in soup.select("article.product_pod h3 a"):
            href = link.get("href")

            if href:
                absolute_url = urljoin(current_url, href)
                book_urls[absolute_url] = current_url

        next_link = soup.select_one("li.next a")

        if next_link and next_link.get("href"):
            current_url = urljoin(
                current_url,
                next_link["href"],
            )
        else:
            current_url = None

    print(
        f"catalogue_pages={catalogue_pages} "
        f"discovered={len(book_urls)} "
        f"unique_urls={len(book_urls)}"
    )

    return book_urls


def normalize_price(price_text: str) -> float:
    """Convert a price such as £51.77 into a numeric value."""

    match = re.search(
        r"(\d+(?:\.\d+)?)",
        price_text,
    )

    if not match:
        raise ValueError(
            f"Could not normalize price: {price_text}"
        )

    return float(match.group(1))


def extract_book_record(
    html: str,
    product_url: str,
    source_page: str,
) -> dict:
    """Extract and normalize one book."""

    soup = BeautifulSoup(html, "html.parser")

    product = soup.select_one("article.product_page")

    if product is None:
        raise ValueError("Product area not found")

    title_element = product.select_one("h1")
    price_element = product.select_one(".price_color")
    availability_element = product.select_one(
        ".availability"
    )
    rating_element = product.select_one(".star-rating")
    description_element = product.select_one(
        "#product_description + p"
    )

    if title_element is None:
        raise ValueError("Title not found")

    if price_element is None:
        raise ValueError("Price not found")

    if availability_element is None:
        raise ValueError("Availability not found")

    if rating_element is None:
        raise ValueError("Rating not found")

    title = title_element.get_text(strip=True)
    price_text = price_element.get_text(strip=True)
    availability_text = availability_element.get_text(
        " ",
        strip=True,
    )

    rating_classes = rating_element.get("class", [])

    rating_text = next(
        (
            class_name
            for class_name in rating_classes
            if class_name != "star-rating"
        ),
        None,
    )

    if rating_text is None:
        raise ValueError("Rating value not found")

    description = (
        description_element.get_text(
            " ",
            strip=True,
        )
        if description_element
        else None
    )

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "price_gbp": normalize_price(price_text),
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }


def fetch_book_pages(
    book_urls: dict[str, str],
) -> tuple[list[dict], list[dict]]:
    """Fetch books while isolating individual failures."""

    records = []
    failures = []

    for index, (product_url, source_page) in enumerate(
        book_urls.items(),
        start=1,
    ):
        cache_file = CACHE_DIR / f"book-{index}.html"

        try:
            html, from_cache = fetch_page(
                product_url,
                cache_file,
            )

            record = extract_book_record(
                html=html,
                product_url=product_url,
                source_page=source_page,
            )

            records.append(record)

            if not from_cache and index < len(book_urls):
                sleep(REQUEST_DELAY)

        except Exception as exc:
            print(
                f"FAILED: {product_url} — {exc}"
            )

            failures.append(
                {
                    "url": product_url,
                    "error": str(exc),
                }
            )

    return records, failures


def validate_and_store(
    records: list[dict],
    failures: list[dict],
) -> tuple[int, int]:
    """Validate records and store valid/invalid results."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    valid_records = []
    errors = []

    for record in records:
        try:
            validated = BookRecord.model_validate(record)

            valid_records.append(
                validated.model_dump(mode="json")
            )

        except ValidationError as exc:
            errors.append(
                {
                    "record": record,
                    "reason": exc.errors(),
                }
            )

    unique_records = {}

    for record in valid_records:
        unique_records[str(
            record["product_url"]
        )] = record

    valid_records = list(
        unique_records.values()
    )

    books_file = OUTPUT_DIR / "books.json"
    errors_file = OUTPUT_DIR / "errors.json"

    books_file.write_text(
        json.dumps(
            valid_records,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    errors_file.write_text(
        json.dumps(
            errors,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return len(valid_records), len(errors)


def write_run_report(
    started_at: str,
    duration_seconds: float,
    catalogue_pages: int,
    pages_fetched: int,
    cache_hits: int,
    valid_records: int,
    invalid_records: int,
    failures: list[dict],
) -> None:
    """Write the required run report."""

    report = {
        "started_at": started_at,
        "duration_seconds": round(
            duration_seconds,
            2,
        ),
        "catalogue_pages": catalogue_pages,
        "pages_fetched": pages_fetched,
        "cache_hits": cache_hits,
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "failed_pages": len(failures),
        "failures": failures,
    }

    report_file = OUTPUT_DIR / "run-report.json"

    report_file.write_text(
        json.dumps(
            report,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    print("\nRUN REPORT")
    print(
        f"pages_fetched={pages_fetched}"
    )
    print(
        f"cache_hits={cache_hits}"
    )
    print(
        f"valid_records={valid_records}"
    )
    print(
        f"invalid_records={invalid_records}"
    )
    print(
        f"failed_pages={len(failures)}"
    )
    print(
        f"duration_seconds="
        f"{duration_seconds:.2f}"
    )


def run_scraper() -> None:
    """Run the complete scraper pipeline."""

    start_time = monotonic()

    started_at = datetime.now(
        timezone.utc
    ).isoformat()

    print("Starting polite scraper...\n")

    book_urls = discover_books()

    records, failures = fetch_book_pages(
        book_urls
    )

    valid_records, invalid_records = (
        validate_and_store(
            records,
            failures,
        )
    )

    duration = monotonic() - start_time

    write_run_report(
        started_at=started_at,
        duration_seconds=duration,
        catalogue_pages=3,
        pages_fetched=len(records),
        cache_hits=0,
        valid_records=valid_records,
        invalid_records=invalid_records,
        failures=failures,
    )


if __name__ == "__main__":
    run_scraper()