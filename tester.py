import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
table_headers = ['Region', 'City', 'Establishment Type', 'Title', 'Link']

# Todo - Define a user-agent/header to avoid being blocked
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                  'Safari/537.36'
}


def webscrape():
    """Scrape data using the query, plug key_words into query, create table
    using the given headers, log errors"""
    try:
        url = f"https://www.google.com/search?q=gyms+in+dunedin+otago"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        for result in soup.select('.tF2Cxc'):
            title = result.select_one('.LC20lb').text if result.select_one('.LC20lb') else "No title"
            link = result.select_one('a')['href'] if result.select_one('a') else "No link"
            add_to_table("gym", "Dunedin", "Otago", title, link)

    except requests.exceptions.RequestException as e:
        print("Oops")


def add_to_table(establishment, city, region, title, link):
    """Append the data to a table"""
    data.append({
        'Region': region,
        'City': city,
        'Type': establishment,
        'Title': title,
        'Link': link
    })


webscrape()
for entry in data:
    print(entry)
