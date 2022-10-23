#/bin/python

import sys
sys.path.append('./src')

from time import sleep
import json
import random
import logging
import utils as ut
from scrapper import ScrapperFactory


BASE_URL    = 'https://www.amazon.com/'
CONFIG_PATH = 'config'
OUTPUT_PATH = 'output'
scrapper    = ScrapperFactory.productSearchResult()
logging.basicConfig(level=logging.INFO)


def save(products):
    ut.save_json(f'{OUTPUT_PATH}/product_search_results_output', {'products': products})


def save_html(url, content):
    url = url.replace(BASE_URL, '')
    with open(f'{OUTPUT_PATH}/{url}.html', 'w') as f: f.write(content)


with open(f'{CONFIG_PATH}/product_search_results_urls','r') as urls:
    products = []
    for url in urls.read().splitlines():
        result = scrapper.scrape(url)
        if not result.empty():
            save_html(url, result.html)
            for product in result.json[0]['products']:
                logging.info("Product: %s"%product['title'])
                products.append(product)
        ut.wait()
    save(products)