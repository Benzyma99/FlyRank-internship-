from pathlib import Path
import requests


BASE_URL = "https://books.toscrape.com/"
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
CACHE_FILE = CACHE_DIR / "catalogue-page-1.html"

USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/Benzyma99/FlyRank-internship-)"
TIMEOUT = 10


def fetch_catalogue_page():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    if CACHE_FILE.exists():
        content = CACHE_FILE.read_text(encoding="utf-8")
        print(f"CACHE HIT: {len(content.encode('utf-8'))} bytes")
        return content

    headers = {
        "User-Agent": USER_AGENT
    }

    response = requests.get(
        BASE_URL,
        headers=headers,
        timeout=TIMEOUT,
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Fetch failed: HTTP {response.status_code}"
        )

    CACHE_FILE.write_bytes(response.content)

    print(f"FETCH: {len(response.content)} bytes")

    return response.text


if __name__ == "__main__":
    fetch_catalogue_page()