# The Polite Scraper

## Target Classification

### Target
[Books to Scrape](https://books.toscrape.com/)

### Why this site?
Books to Scrape is a public practice sandbox designed for learning and practicing web scraping.

### Scope
This scraper will process only the first three catalogue pages and discover the books listed on those pages.

The expected scope is:
- 3 catalogue pages
- 60 unique book pages

### Data collected
For each book, the scraper will collect:
- title
- product URL
- price text
- availability text
- rating text
- description
- source catalogue page
- fetch timestamp

A normalized numeric `price_gbp` value will also be produced later in the pipeline.

### Robots.txt check
The requested `https://books.toscrape.com/robots.txt` returned `404 Not Found`.

Therefore, no robots file was found. A missing robots file is not treated as permission to scrape.

### Why this is appropriate
Books to Scrape is specifically provided as a practice sandbox, making it an appropriate target for this learning assignment.

I will not reuse this code on another site without checking its rules and terms first.