"""
Nathan Scott
Webscrape Project

Main:
    - Mediates process from input query to output data
    - Accesses individual modules
    - Mediates access to objects between classes/modules
"""
import random
import time
from request_query import *
from process_query import *
from create_spreadsheet import *


"""
The process of webscraping for data is as follows:

1.  Define the headers for final spreadsheet
2.  Build a list of queries
3.  Request next query if list not empty
4.  Process the query
5.  If allowed, return to step 2
6.  When webscraping completed, create spreadsheet
"""


def start_scraping():
    """Start scraping ;)"""
    build_query_list(regions, types)
    next_query_request = next_query()
    while next_query_request is not None:
        region, city, establishment = next_query_request
        webscrape(region, city, establishment)
        time.sleep(random.uniform(1, 3))
        next_query_request = next_query()
    table_data = fetch_table()
    create_csv(table_data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    start_scraping()
