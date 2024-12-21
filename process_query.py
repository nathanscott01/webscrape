"""
Nathan Scott
Webscrape Project

Process Query:
    - Perform a webscrape using the query
    - Log errors
    - Create a table containing the new data
    - Update a master table periodically
    - Add functionality to switch between API and personal janky setup
"""

import requests
from dotenv import load_dotenv
import os
import logging


# Load API key from .env
load_dotenv()
API_KEY = os.getenv('BRIGHT_DATA_API_KEY')


# Todo - Configure Logging
logging.basicConfig(
    filename='scraping_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Todo - Initialise data object
data = []
SERP_API_ENDPOINT = 'https://api.brightdata.com/serp'
table_headers = ['Region', 'City', 'Establishment Type', 'Title', 'Link']

# # Todo - Define a user-agent/header to avoid being blocked
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
#                   'Safari/537.36'
# }


def webscrape(region, city, establishment_type, retries=3):
    """Scrape data using the query, plug key_words into query, create table
    using the given headers, log errors"""
    query = f"{establishment_type} in {city} {region} New Zealand"

    # Payload to be sent to Bright Data API
    payload = {
        "query": query,
        "location": f"{city}, {region}, New Zealand",
        "language": "en",
        "device": "desktop"
    }

    # Headers with Authorization Token
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    for attempt in range(retries):
        try:
            # url = f"https://www.google.com/search?q={query.replace(' ', '+')}"

            # response = requests.get(url, headers=headers)
            response = requests.post(SERP_API_ENDPOINT, headers=headers, json=payload)

            # Handle 429 Error (Rate Limit)
            if response.status_code == 429:
                logging.warning(f"Rate limit hit for {query}. Retrying in 10 seconds (Attempt {attempt + 1}/{retries})...")
                time.sleep(10)  # Wait before retrying
                continue  # Retry the request

            response.raise_for_status()  # Raise HTTPError for bad responses
            search_results = response.json()

            # soup = BeautifulSoup(response.text, 'html.parser')
            # for result in soup.select('.tF2Cxc'):
            #     title = result.select_one('.LC20lb').text if result.select_one('.LC20lb') else "No title"
            #     link = result.select_one('a')['href'] if result.select_one('a') else "No link"
            #     add_to_table("gym", "Dunedin", "Otago", title, link)

            for result in search_results.get('organic search', []):
                title = result.get('title', 'No title')
                link = result.get('link', 'No link')
                add_to_table(establishment_type, city, region, title, link)

        except requests.exceptions.RequestException as e:
            # Log connection or HTTP errors
            logging.error(f"Error scraping {query} on attempt {attempt+1}: {e}")
            if attempt == retries - 1:
                logging.error(f"Max retries reached for {query}. Skipping...")

        except Exception as e:
            # Log unexpected errors
            logging.error(f"Unexpected error for {query}: {e}")


def add_to_table(establishment, city, region, title, link):
    """Append the data to a table"""
    data.append({
        'Region': region,
        'City': city,
        'Type': establishment,
        'Title': title,
        'Link': link
    })


def fetch_table():
    """Fetch the table"""
    return data
