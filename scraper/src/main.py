from datetime import datetime, timezone
from pathlib import Path
from time import sleep
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


BASE_URL = "https://books.toscrape.com/"
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"

USER_AGENT = (
    "FlyRankInternship-A9/1.0 "
    "(+https://github.com/Benzyma99/FlyRank-internship-)"
)
TIMEOUT = 10
REQUEST_DELAY = 0.5


def fetch_page(url: str, cache_file: Path) -> tuple[str, bool]:
    """Fetch a page or read it from cache.

    Returns:
        tuple[str, bool]: HTML content and whether it came from cache.
    """

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if cache_file.exists():
        content = cache_file.read_text(encoding="utf-8")
        print(f"CACHE HIT: {url} ({len(content.encode('utf-8'))} bytes)")
        return content, True

    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Fetch failed: HTTP {response.status_code} for {url}"
        )

    cache_file.write_bytes(response.content)

    print(f"FETCH: {url} ({len(response.content)} bytes)")

    return response.text, False


def discover_books():
    """Discover book URLs from the first three catalogue pages."""

    current_url = BASE_URL
    catalogue_pages = 0
    book_urls = {}

    while current_url and catalogue_pages < 3:
        catalogue_pages += 1

        cache_file = CACHE_DIR / f"catalogue-page-{catalogue_pages}.html"
        html, _ = fetch_page(current_url, cache_file)

        soup = BeautifulSoup(html, "html.parser")

        for link in soup.select("article.product_pod h3 a"):
            href = link.get("href")

            if href:
                absolute_url = urljoin(current_url, href)
                book_urls[absolute_url] = current_url

        next_link = soup.select_one("li.next a")

        if next_link and next_link.get("href"):
            current_url = urljoin(current_url, next_link["href"])
        else:
            current_url = None

    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(book_urls)}")
    print(f"unique_urls={len(book_urls)}")

    return book_urls


def extract_book_record(
    html: str,
    product_url: str,
    source_page: str,
) -> dict:
    """Extract the required raw fields from one book page."""

    soup = BeautifulSoup(html, "html.parser")

    product = soup.select_one("article.product_page")

    if product is None:
        raise ValueError("Product area not found")

    title_element = product.select_one("h1")
    price_element = product.select_one(".price_color")
    availability_element = product.select_one(".availability")
    rating_element = product.select_one(".star-rating")
    description_element = product.select_one("#product_description + p")

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
    availability_text = availability_element.get_text(" ", strip=True)

    rating_classes = rating_element.get("class", [])
    rating_text = next(
        (
            class_name
            for class_name in rating_classes
            if class_name != "star-rating"
        ),
        None,
    )

    description = (
        description_element.get_text(" ", strip=True)
        if description_element
        else None
    )

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }


def fetch_book_pages(book_urls: dict[str, str]) -> list[dict]:
    """Fetch and extract all discovered book pages."""

    records = []

    for index, (product_url, source_page) in enumerate(
        book_urls.items(),
        start=1,
    ):
        cache_file = CACHE_DIR / f"book-{index}.html"

        try:
            html, from_cache = fetch_page(product_url, cache_file)

            record = extract_book_record(
                html=html,
                product_url=product_url,
                source_page=source_page,
            )

            records.append(record)

            if not from_cache and index < len(book_urls):
                sleep(REQUEST_DELAY)

        except Exception as exc:
            print(f"FAILED: {product_url} — {exc}")

    return records


if __name__ == "__main__":
    book_urls = discover_books()

    records = fetch_book_pages(book_urls)

    print(f"detail_pages={len(records)}")

    if records:
        print("\nSample raw record:")
        print(records[0])