import urllib.robotparser
from urllib.error import HTTPError
from urllib.parse import urlparse
import time
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

# Cache for robots.txt
robots_cache = {}
CACHE_TIMEOUT = 3600  # 1 hour

def get_robots_parser(base_url):
    if base_url in robots_cache and time.time() - robots_cache[base_url]["timestamp"] < CACHE_TIMEOUT:
        return robots_cache[base_url]["parser"]

    robots_url = f"{base_url}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        print("robots.txt found")
    except HTTPError as e:
        if e.code == 404:
            print("robots.txt not found. Assuming access is allowed.")
            rp = None  # Or a default allow/disallow parser
        else:
            print(f"Error reading robots.txt: {e}")
            rp = None

    if rp:
        robots_cache[base_url] = {"parser": rp, "timestamp": time.time()}

    return rp

def scrape_website(url, user_agent):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    rp = get_robots_parser(base_url)

    if rp is None or rp.can_fetch(user_agent, url):  # Allow if no robots.txt or allowed
        try:
            response = requests.get(url, headers={"User-Agent": user_agent})
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Example: Extract quotes and authors from quotes.toscrape.com
            quotes = soup.find_all('div', class_='quote')
            for quote in quotes:
                text = quote.find('span', class_='text').text
                author = quote.find('small', class_='author').text
                print(f"Quote: {text}")
                print(f"Author: {author}")
                print("-" * 20)

            # Pagination handling:
            next_page = soup.find('li', class_='next')
            if next_page:
                next_page_link = next_page.find('a')['href']
                next_page_url = base_url + next_page_link

                # Check robots.txt *before* scraping the next page:
                parsed_next_url = urlparse(next_page_url)
                rp_next = get_robots_parser(parsed_next_url.scheme + "://" + parsed_next_url.netloc) # Parse robots.txt for the base url of the next page
                if rp_next is None or rp_next.can_fetch(user_agent, next_page_url):  # Check if allowed
                    scrape_website(next_page_url, user_agent)  # Scrape if allowed
                else:
                    print(f"Not allowed to scrape {next_page_url} (robots.txt)")
                    # break  # Uncomment to stop pagination on disallowed page.

            # Respect Crawl-delay
            if rp:
                crawl_delay = rp.crawl_delay(user_agent)
                if crawl_delay:
                    print(f"Waiting for {crawl_delay} seconds...")
                    time.sleep(crawl_delay)
                else:
                    time.sleep(1)  # Default delay

        except RequestException as e:
            print(f"Error fetching {url}: {e}")
    else:
        print(f"Not allowed to scrape {url} according to robots.txt")



my_user_agent = "MyWebScraperBot/1.0 (me@example.com)" # Replace with your info
base_url = "https://quotes.toscrape.com/" # Start scraping from the base URL
scrape_website(base_url, my_user_agent)