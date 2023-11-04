import traceback
import cloudscraper
import pandas as pd
import random
import time
from bs4 import BeautifulSoup
import re
import csv
import json

def data_scraper_redirect(scraper, url):
    response = scraper.get(url)
    if response.status_code == 200:
        page_source = response.text
        soup = BeautifulSoup(page_source, 'html.parser')
    else:
        print("fail to open")
        soup = None
    return soup
def find_soup():
    scraper = cloudscraper.create_scraper()
    url = 'https://www.cambridge.org/core/journals/journal-of-economic-history/all-issues'
    soup = data_scraper_redirect(scraper, url)
    return(soup)

def find_link(soup,journal_name):
    article_url_list = []
    for link in soup.find_all('a', href=re.compile("^/core")):
        href = link.get('href')
        article_url = 'https://www.cambridge.org' + href
        article_url_list.append(article_url)
        with open(f'{journal_name}_all_issues.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            for url in article_url_list:
                writer.writerow([url])
    print("successfully write url to file")

soup = find_soup()
find_link(soup,"The Journal of Economic History")