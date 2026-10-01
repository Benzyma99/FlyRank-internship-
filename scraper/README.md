# The Polite Scraper

## Target Classification

### Target

[Books to Scrape](https://books.toscrape.com/)

### Why this site?

Books to Scrape is a public practice sandbox designed for learning and practicing web scraping.

### Scope

This scraper processes only the first three catalogue pages.

Expected scope:

- 3 catalogue pages
- 60 unique book pages

### Data collected

For each book, the scraper collects:

- title
- product URL
- price text
- availability text
- rating text
- description
- source catalogue page
- fetch timestamp

The pipeline also normalizes the price into:

- `price_gbp`

## Robots.txt Check

The requested:

`https://books.toscrape.com/robots.txt`

returned `404 Not Found`.

Therefore, no robots file was found. A missing robots file is not treated as permission to scrape.

Books to Scrape is specifically provided as a practice sandbox for scraping exercises.

I will not reuse this code on another site without checking its rules and terms first.

## Installation

Python 3.10+ is required.

Install the dependencies:

```powershell
python -m pip install requests beautifulsoup4 pydantic

## Submission Verification

Before submission, the scraper was verified to:

- process exactly 3 catalogue pages
- discover 60 unique book URLs
- extract 60 book detail pages
- produce 60 valid records
- produce 0 invalid records during the successful run
- isolate failed pages
- avoid retrying 403 and 404 responses
- retry once for timeout/5xx failures
- cache downloaded HTML
- keep cache files out of Git
- produce a run report
- use a descriptive User-Agent
- maintain a request delay for real requests
- produce repeatable output on reruns