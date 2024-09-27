import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv

# Function to extract all URLs from the sitemap asynchronously
async def get_sitemap_urls(session, sitemap_url):
    """Extract all URLs from the sitemap, including nested sitemaps."""
    urls = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    print(f"Fetching sitemap: {sitemap_url}")
    try:
        async with session.get(sitemap_url, headers=headers, timeout=10) as response:
            print(f"Response Code: {response.status}")
            if response.status != 200:
                print(f"Failed to access {sitemap_url} with status: {response.status}")
                return urls

            content = await response.text()
            soup = BeautifulSoup(content, 'xml')

            # Check for nested sitemaps
            for sitemap in soup.find_all('sitemap'):
                sitemap_loc = sitemap.find('loc').text
                print(f"Found nested sitemap: {sitemap_loc}")
                urls.extend(await get_sitemap_urls(session, sitemap_loc))

            # Get URLs from current sitemap
            for url in soup.find_all('url'):
                loc = url.find('loc').text
                urls.append(loc)
                print(f"Found URL: {loc}")
    
    except asyncio.TimeoutError:
        print(f"Timeout occurred while accessing {sitemap_url}")
    except aiohttp.ClientError as e:
        print(f"Client error occurred while fetching sitemap: {e}")
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
    
    return urls

# Function to extract links from a page asynchronously
async def extract_links_from_page(session, page_url):
    """Scrape the page and return all URLs found in the body."""
    links = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    print(f"Scraping page: {page_url}")
    try:
        async with session.get(page_url, headers=headers, timeout=10) as response:
            print(f"Page response code: {response.status}")
            if response.status != 200:
                print(f"Failed to load page: {page_url}")
                return links

            content = await response.text()
            soup = BeautifulSoup(content, 'html.parser')

            # Extract all anchor tags and convert relative links to absolute
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                full_url = urljoin(page_url, href)  # Handle relative URLs
                links.append(full_url)
                print(f"Found link: {full_url}")
    
    except asyncio.TimeoutError:
        print(f"Timeout occurred while scraping page {page_url}")
    except aiohttp.ClientError as e:
        print(f"Client error occurred while fetching page: {e}")
    except Exception as e:
        print(f"Error fetching page content for {page_url}: {e}")
    
    return links

# Function to check URL status asynchronously
async def check_url_status(session, url):
    """Check if the URL is valid or not."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    try:
        async with session.get(url, headers=headers, allow_redirects=True, timeout=10) as response:
            print(f"Checked URL: {url} - Status Code: {response.status}")
            return response.status
    except asyncio.TimeoutError:
        print(f"Timeout occurred while checking URL {url}")
        return None
    except aiohttp.ClientError as e:
        print(f"Client error occurred while checking URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Error checking URL {url}: {e}")
        return None

# Function to generate a CSV report
def generate_report(invalid_urls, filename="invalid_links_report.csv"):
    """Generate a CSV report of invalid URLs."""
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Invalid URL', 'Page URL', 'Status Code'])
            for invalid_url, page_url, status_code in invalid_urls:
                writer.writerow([invalid_url, page_url, status_code])
        print(f"Report saved as {filename}")
    except Exception as e:
        print(f"Error saving report: {e}")

# Main async function to drive the process
async def main(sitemap_url):
    # Create a session to reuse across requests
    async with aiohttp.ClientSession() as session:
        # Step 1: Extract all URLs from the sitemap
        print("Starting sitemap extraction...")
        sitemap_urls = await get_sitemap_urls(session, sitemap_url)
        
        if not sitemap_urls:
            print("No URLs found in sitemap.")
            return
        
        invalid_urls = []

        # Step 2: Scrape each URL and find links in the body
        for page_url in sitemap_urls:
            print(f"\nProcessing page: {page_url}")
            page_links = await extract_links_from_page(session, page_url)
            
            # Step 3: Check each link's status asynchronously
            check_tasks = [check_url_status(session, link) for link in page_links]
            status_codes = await asyncio.gather(*check_tasks)

            # Collect invalid URLs
            for link, status_code in zip(page_links, status_codes):
                if status_code and status_code != 200:
                    invalid_urls.append((link, page_url, status_code))
                    print(f"Invalid link found: {link} on page {page_url} with status {status_code}")

        # Step 4: Generate report for invalid URLs
        if invalid_urls:
            generate_report(invalid_urls)
        else:
            print("No invalid URLs found.")

# Example usage
if __name__ == "__main__":
    sitemap_url = 'https://i-golf-pro.com/sitemap_index.xml'  # Replace with your sitemap URL
    
    # Run the main event loop
    asyncio.run(main(sitemap_url))
