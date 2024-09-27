# Sitemap URL Scraper and Validator

## Introduction

This Python script performs the following tasks:

1. **Sitemap URL Extraction**: Fetches all URLs from a sitemap (supports nested sitemaps).
2. **Page Link Scraping**: For each URL in the sitemap, it scrapes all links present in the page content.
3. **Link Validation**: Checks the status code of each link (e.g., 200, 404) to verify if it's valid or broken.
4. **Report Generation**: Generates a CSV report containing invalid links, the pages where they were found, and their status codes.

The script is designed to handle both single-level and multi-level sitemaps, making asynchronous HTTP requests to improve speed.

## Prerequisites

- **Python 3.7+**
- **Dependencies**:
  - `aiohttp`: For asynchronous HTTP requests.
  - `beautifulsoup4`: For parsing HTML and XML.
  - `lxml`: For efficient parsing of XML and HTML documents.
  
To install these dependencies, use the following pip command:

```bash
pip install aiohttp beautifulsoup4 lxml
```

## How the Script Works

### Workflow:

#### Sitemap URL Extraction:
- The script begins by fetching the sitemap (in XML format).
- It parses the sitemap using BeautifulSoup with the `lxml` parser to extract URLs.
- If nested sitemaps are found, it recursively fetches those as well.

#### Scraping Links from Pages:
- For each URL from the sitemap, the script makes an HTTP request to the page.
- It scrapes all hyperlinks (`<a>` tags) within the page content, converting any relative URLs to absolute URLs.

#### Link Validation:
- For each link found on a page, the script checks its HTTP status code (e.g., 200 for OK, 404 for Not Found).
- It marks any links with non-200 status codes as invalid.

#### CSV Report:
- The script collects all invalid links and generates a CSV report with the following columns:
  - **Invalid URL**: The broken or invalid URL.
  - **Page URL**: The page where the invalid link was found.
  - **Status Code**: The HTTP status code of the invalid link.

### Key Components:

#### `get_sitemap_urls(session, sitemap_url)`:
- Asynchronously fetches and parses the sitemap to extract URLs. Recursively handles nested sitemaps.

#### `extract_links_from_page(session, page_url)`:
- Scrapes all hyperlinks from a page and converts relative URLs to absolute ones.

#### `check_url_status(session, url)`:
- Validates the URL by checking its HTTP status code.

#### `generate_report(invalid_urls, filename)`:
- Generates a CSV file containing all invalid links.

### Main Workflow:
- The script first extracts the sitemap URLs, then scrapes links from each page, checks their validity, and finally generates a report.

### CSV Report:
- The CSV report will contain the following columns:
  - **Invalid URL**: The URL that returned an invalid status code.
  - **Page URL**: The URL of the page where the invalid link was found.
  - **Status Code**: The HTTP status code (e.g., 404 for Not Found).

## Running the Script

1. Clone or download this repository.
2. Install the required dependencies:

```bash
   pip install aiohttp beautifulsoup4 lxml
```
3. Update the sitemap_url in the script with your desired sitemap URL.

4. Run the script:
5. After the script finishes, a CSV report named invalid_links_report.csv will be generated in the current directory.

```python
if __name__ == "__main__":
    sitemap_url = 'https://i-golf-pro.com/sitemap_index.xml'
    asyncio.run(main(sitemap_url))
```


