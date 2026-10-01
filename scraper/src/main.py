from pathlib import Path
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


def fetch_page(url: str, cache_file: Path) -> str:
    """Fetch a page or read it from cache."""

    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if cache_file.exists():
        content = cache_file.read_text(encoding="utf-8")
        print(f"CACHE HIT: {url} ({len(content.encode('utf-8'))} bytes)")
        return content

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

    return response.text


def discover_books():
    """Discover book URLs from the first three catalogue pages."""

    current_url = BASE_URL
    catalogue_pages = 0
    book_urls = set()

    while current_url and catalogue_pages < 3:
        catalogue_pages += 1

        cache_file = CACHE_DIR / f"catalogue-page-{catalogue_pages}.html"
        html = fetch_page(current_url, cache_file)

        soup = BeautifulSoup(html, "html.parser")

        # Find every book link on this catalogue page.
        for link in soup.select("article.product_pod h3 a"):
            href = link.get("href")

            if href:
                absolute_url = urljoin(current_url, href)
                book_urls.add(absolute_url)

        # Find the catalogue's own "next" link.
        next_link = soup.select_one("li.next a")

        if next_link and next_link.get("href"):
            current_url = urljoin(current_url, next_link["href"])
        else:
            current_url = None

    print(f"catalogue_pages={catalogue_pages}")
    print(f"discovered={len(book_urls)}")
    print(f"unique_urls={len(book_urls)}")

    return book_urls


if __name__ == "__main__":
    discover_books()