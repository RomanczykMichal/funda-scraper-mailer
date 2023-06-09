from funda_scraper import FundaScraper
from logger import logger
import gc
import time
from mailer import Mailer
import argparse
import configparser
import pandas as pd
from datetime import datetime, timedelta
import os

EMAIL_SENDER = os.environ["FS_EMAIL_SENDER"]
EMAIL_PASS = os.environ["FS_EMAIL_PASS"]
CONFIG_PATH = './config.ini'
LAST_DATE_FOUND = '1970-01-01 00:00:00.000000'

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--time", type=int, required=True, help='time interval between messeges (in minutes).')
    parser.add_argument("-a", "--area", type=str, required=True, help='area to search.')
    parser.add_argument("-r", "--range", type=int, default=0, help='additional area to search.')
    parser.add_argument("-n", "--n_pages", type=int, default=3, help='number of pages to search.')
    parser.add_argument("-m", "--mail", type=str, required=True, help='email of receiver.')
    parser.add_argument("-s", "--subject", type=str, default='New Ads funda.nl', help='subject of the email.')
    return parser.parse_args()

def init_config():
    config = configparser.ConfigParser()
    config_file = config.read(CONFIG_PATH)
    if not config_file:
        config.add_section("data")
        config.set("data", "last_date_found", LAST_DATE_FOUND)
        config.add_section("houses_today")
        config.set('houses_today', 'todays_date', str(datetime.now().date() - timedelta(days=1)))
        write_config_file(config)
    return config

def set_config_pair(config, section, key, value):
    config.set(section, key, value)

def write_config_file(config):
    with open("config.ini", 'w') as path:
                config.write(path)

def validate_config_section(config, todays_date):
     if config["houses_today"].get('todays_date') != str(todays_date):
        config.remove_section('houses_today')
        config.add_section("houses_today")
        config.set('houses_today', 'todays_date', str(datetime.now().date() - timedelta(days=1)))
        write_config_file(config)

if __name__ == "__main__":
    args = init_parser()
    config = init_config()
    todays_date = datetime.now().date() - timedelta(days=1)
    validate_config_section(config=config, todays_date=todays_date)
    last_date_found = config["data"].get('last_date_found')

    scraper = FundaScraper(area=args.area, want_to="rent", find_past=False, n_pages=args.n_pages, area_range=args.range, sort_type='sorteer-datum-af', log_disabled=True)

    while True:
        logger.info('*** Scrape started ***')
        scraped_data = scraper.run()
        logger.info('*** Scrape finished ***')
        scraped_data['date_list'] = pd.to_datetime(scraped_data['date_list']).dt.date

        #TODO TESTING
        filtered_scraped_data = scraped_data.loc[(scraped_data['date_list'] >= pd.to_datetime(last_date_found).date())]
        
        todays = scraped_data.loc[(scraped_data['date_list'] == todays_date)]
        for index, row in todays.iterrows():
            if not config.has_option('houses_today', str(row['house_id'])):
                set_config_pair(config, 'houses_today', str(row['house_id']), 'checked')
            else:
                filtered_scraped_data = filtered_scraped_data.loc[(filtered_scraped_data['house_id'] != row['house_id'])]
        write_config_file(config)

        if len(filtered_scraped_data.index) > 1:
            last_date_found = filtered_scraped_data.iloc[0]['date_list']
            set_config_pair(config, 'data', 'last_date_found', str(last_date_found))
            write_config_file(config)
            Mailer.send_mail(EMAIL_SENDER, args.mail, EMAIL_PASS, args.subject, filtered_scraped_data)
            logger.info('*** Wysłano wiadomość email ***')
        else:
            logger.info('*** Nie znaleziono nowych ogłoszeń ***')

        time.sleep(args.time * 60)
        gc.collect()
    