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
import time
from bs4 import BeautifulSoup


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
url = "https://api.brightdata.com/request"
table_headers = ['Region', 'City', 'Establishment Type', 'Title', 'Link']


def webscrape(region, city, establishment_type, retries=3):
    """Scrape data using the query, plug key_words into query, create table
    using the given headers, log errors"""
    # search_query = f"{establishment_type}+in+{city}+{region}+New+Zealand"

    search_query = f"{establishment_type} in {city} {region} New Zealand"
    search_query = search_query.replace(" ", "+")  # Replace all spaces with '+'

    payload = {
        "url": f"https://www.google.com/search?q={search_query}",
        "format": "raw",
        "method": "GET",
        "zone": "my_personal_project"
    }

    # Headers with Authorization Token
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    for attempt in range(retries):
        try:
            response = requests.request("POST", url, json=payload, headers=headers)

            # Handle 429 Error (Rate Limit)
            if response.status_code == 429:
                logging.warning(f"Rate limit hit for {search_query}. Retrying in 10 seconds (Attempt {attempt + 1}"
                                f"/{retries})...")
                time.sleep(10)  # Wait before retrying
                continue  # Retry the request

            response.raise_for_status()  # Raise HTTPError for bad responses
            soup = BeautifulSoup(response.text, 'html.parser')

            # Reuse the old logic to extract organic results
            for result in soup.select('.tF2Cxc'):
                title = result.select_one('.LC20lb').text if result.select_one('.LC20lb') else "No title"
                link = result.select_one('a')['href'] if result.select_one('a') else "No link"
                add_to_table(establishment_type, city, region, title, link)
            break

        except requests.exceptions.RequestException as e:
            # Log connection or HTTP errors
            logging.error(f"Error scraping {search_query} on attempt {attempt+1}: {e}")

            # Log final error and skip to next query if max retries are reached
            if attempt == retries - 1:
                logging.error(f"Max retries reached for {search_query}. Skipping...")

        except Exception as e:
            # Log unexpected errors
            logging.error(f"Unexpected error for {search_query}: {e}")
            break


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
