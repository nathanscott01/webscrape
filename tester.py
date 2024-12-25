import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

# Load API key from .env
load_dotenv()
API_KEY = os.getenv('BRIGHT_DATA_API_KEY')


url = "https://api.brightdata.com/request"
data = []
table_headers = ['Region', 'City', 'Establishment Type', 'Title', 'Link']


def webscrape(region, city, establishment_type):
    """Scrape data using the query, plug key_words into query, create table using the given headers, log errors"""
    search_query = f"{establishment_type}+in+{city}+{region}+New+Zealand"

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

    response = requests.request("POST", url, json=payload, headers=headers)
    response.raise_for_status()  # Raise HTTPError for bad responses

    # Process HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Reuse the old logic to extract organic results
    for result in soup.select('.tF2Cxc'):
        title = result.select_one('.LC20lb').text if result.select_one('.LC20lb') else "No title"
        link = result.select_one('a')['href'] if result.select_one('a') else "No link"
        add_to_table(establishment_type, city, region, title, link)


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
