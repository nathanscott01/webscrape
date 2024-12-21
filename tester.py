import requests
from dotenv import load_dotenv
import os
import time
import logging

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('BRIGHT_DATA_API_KEY')


# Load in SSL Certificate
CA_CERT_PATH = os.path.join(os.path.dirname(__file__), 'brightdata_ca.crt')

data = []
table_headers = ['Region', 'City', 'Establishment Type', 'Title', 'Link']
SERP_API_ENDPOINT = 'https://api.brightdata.com/serp-api'


# Configure Logging
logging.basicConfig(
    filename='scraping_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def webscrape(region, city, establishment_type, retries=3):
    """Scrape data using the query, plug key_words into query, create table using the given headers, log errors"""
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
            response = requests.post(
                SERP_API_ENDPOINT,
                headers=headers,
                json=payload,
                verify=CA_CERT_PATH
            )

            # Handle 429 Error (Rate Limit)
            if response.status_code == 429:
                logging.warning(f"Rate limit hit for {query}. Retrying in 10 seconds (Attempt {attempt + 1}/{retries})...")
                time.sleep(10)  # Wait before retrying
                continue  # Retry the request

            response.raise_for_status()  # Raise HTTPError for bad responses
            search_results = response.json()

            for result in search_results.get('organic_results', []):
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


webscrape('Otago', 'Dunedin', 'Gyms')
for entry in data:
    print(entry)
# print(API_KEY)
# webscrape()
