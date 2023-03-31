import importlib
import logging
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_scraper_modules():
    """
    Returns a list of all scraper modules present in the `scrapers` package
    """
    logging.info('start of get_scraper_modules')
    scraper_modules = []
    for file in os.listdir("./code"):
        if file.endswith("_scraper.py"):
            module_name = file[:-3]  # Remove the ".py" extension
            scraper_module = importlib.import_module(f"{module_name}")
            scraper_modules.append(scraper_module)
    logging.debug('scraper_modules is ' + scraper_modules.__str__())
    return scraper_modules


def save_to_csv(data, file_path):
    """
    Saves a dataframe to a csv file at the specified file path. If the directory
    does not exist, it creates the directory before saving the file.

    Args:
    data: pandas.DataFrame - The dataframe to save to a csv file
    file_path: str - The file path to save the csv file to
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    data.to_csv(file_path, index=False)


def read_csv(file_path):
    """
    Reads a csv file into a pandas dataframe.

    Args:
    file_path: str - The file path to read the csv file from

    Returns:
    A pandas.DataFrame containing the data from the csv file
    """
    return pd.read_csv(file_path)


def get_soup(url):
    """
    Sends a GET request to the given URL and returns a BeautifulSoup object
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def extract_table_data(table_divs):
    """
    Extracts data from the table divs and returns a list of table data
    """
    table_data = []

    for table in table_divs:
        rows = table.find('tbody').find_all('tr')
        table_rows = []
        for row in rows[:-1]:
            cols = row.find_all('td')
            cols = [col.text.strip() for col in cols]
            cols.append(table['id'][4:][:3] + ' ' + table['id'][4:][-4:])
            table_rows.append(cols)
        table_data += table_rows

    return table_data
