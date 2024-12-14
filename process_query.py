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
import pandas
from bs4 import BeautifulSoup
import time
import logging

# Todo - Configure Logging

# Todo - Initialise data object

# Todo - Define a user-agent/header to avoid being blocked


def webscrape(query, key_words, table_headers):
    """Scrape data using the query, plug key_words into query, create table
    using the given headers, log errors"""
    return NotImplementedError


def append_table(new_data):
    """Append the new data to main data table"""
