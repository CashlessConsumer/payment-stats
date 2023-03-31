import os
from datetime import date

import logging
import pandas as pd
import scraper_utils
from bs4 import BeautifulSoup

# Define the URL to scrape
url = 'https://www.npci.org.in/what-we-do/e-rupi/product-statistics'


def run():
    logging.info('start of run scraper')
    soup = scraper_utils.get_soup(url)

    table_divs = soup.find_all('div', attrs={'class': 'hideDD'})

    table_data = []
    table_data = scraper_utils.extract_table_data(table_divs)

    # Create a dataframe from the table data
    df = pd.DataFrame(table_data, columns=[
                      'S No', 'Issuer', 'Issued vouchers', 'Redeemed Vouchers', 'Month'])

    df = clean_table_data(df)
    aggregate_df = aggregate_table_data(df)

    output_folder = 'data/eRUPI'
    output_file = f'{output_folder}/ERupi_Statistics.csv'
    aggregate_output_file = f'{output_folder}/ERupi_Aggregate_Statistics.csv'

    scraper_utils.save_to_csv(df, output_file)
    scraper_utils.save_to_csv(aggregate_df, aggregate_output_file)


def clean_table_data(df):
    """
    Cleans the table data and returns a cleaned dataframe
    """
    logging.info('start of clean_table_data')
    df['Issued vouchers'] = df['Issued vouchers'].apply(
        lambda x: x.replace(',', ''))
    df['Redeemed Vouchers'] = df['Redeemed Vouchers'].apply(
        lambda x: x.replace(',', ''))
    df['Issued vouchers'] = df['Issued vouchers'].apply(
        pd.to_numeric, errors='coerce')
    df['Redeemed Vouchers'] = df['Redeemed Vouchers'].apply(
        pd.to_numeric, errors='coerce')
    df['Issuer'] = df['Issuer'].apply(lambda x: str(x).strip())
    df.sort_values(by='Issued vouchers', ascending=False)

    return df


def aggregate_table_data(df):
    """
    Aggregates the table data and returns an aggregated dataframe
    """
    logging.info('start of aggregate_table_data')
    aggregate_df = df.groupby(by='Issuer').sum().sort_values(
        by=['Issued vouchers', 'Issuer'], ascending=False)
    aggregate_df['Redumption Percentage'] = round(
        aggregate_df['Redeemed Vouchers'] / aggregate_df['Issued vouchers'] * 100, 2)

    return aggregate_df
