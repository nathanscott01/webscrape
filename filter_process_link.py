"""
Nathan Scott
Webscrape Project

This program checks the original scraped list and filters legitimite
businesses and attempts to record contact details
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urlparse

# Load scraped data
filename = 'scraped_hydra_data.xlsx'
sheet_name = 'Original'
output_sheet_name = 'Filtered and Processed Links'

exclude_keywords = ['yellowpages', 'tripadvisor', 'foursquare', 'top10', 'directory', 'finda']
include_keywords = ['gym', 'supplement store', 'pilates studio', 'yoga studio', 'pharmacy', 'health store']


email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
phone_pattern = re.compile(r'\+?\d{1,4}?[-.\s\(\)]*\d{1,4}[-.\s\(\)]*\d{1,4}[-.\s\(\)]*\d{1,9}')


def load_data(file, sheet):
    df = pd.read_excel(file, sheet_name=sheet)
    return df


def visit_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return None


def parse_and_filter(url, html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extract text, title and meta descriptions
    title = soup.title.string if soup.title else 'No Title'
    body_text = ' '.join(soup.stripped_strings).lower()
    meta_description = ' '.join([meta.get('content', '').lower() for meta in soup.find_all('meta')])

    # Exclude rubbish links
    if any(keyword in url for keyword in exclude_keywords):
        return None

    # Check if include keywords are in title, body or description
    if any(keyword in title.lower() or keyword in body_text for keyword in include_keywords):
        print(f"Relevant site found: {url}")
        email = email_pattern.search(body_text)
        phone = phone_pattern.search(body_text)
        return {
            'URL': url,
            'Title': title,
            'Email': email.group(0) if email else 'N/A',
            'Phone': phone.group(0) if phone else 'N/A'
        }

    print(f"Irrelevant site: {url}")
    return None


def process_links(df):
    filtered_results = []
    for index, row in df.iterrows():
        url = row.get('Link')
        if not url:
            continue

        # Ensure URL has http/https
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            url = f"https://{url}"

        html = visit_page(url)
        if html:
            business_info = parse_and_filter(url, html)
            if business_info:
                filtered_results.append(business_info)

    return pd.DataFrame(filtered_results)


def save_filterd_data(filtered_df):
    # Save filtered data to a new sheet
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        filtered_df.to_excel(writer, sheet_name=output_sheet_name, index=False)

    print(f"Filtered data written to '{output_sheet_name}' in {filename}")


def filter_processed_data():
    df = load_data(filename, sheet_name)
    filtered_df = process_links(df)
    save_filterd_data(filtered_df)


filter_processed_data()
