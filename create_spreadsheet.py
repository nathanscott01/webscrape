"""
Nathan Scott
Webscrape Algorithm

Create Spreadsheet:
    - Take a data set and create a .xlsx or .csv spreadsheet
"""

import xlsxwriter
import pandas as pd


def create_csv(data):
    """Create a csv file using the given data"""
    results_df = pd.DataFrame(data)
    results_df.to_csv('scraped_fitness_data.csv', index=False)


def create_excel_sheet(data, spreadsheet_name, column_format):
    """Create an Excel file using the given data and column formats"""
    return NotImplementedError
