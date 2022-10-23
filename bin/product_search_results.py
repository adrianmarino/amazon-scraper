#/bin/python

import sys
sys.path.append('./src')

from time import sleep
import json
import random
import logging
import utils as ut
from scrapper import ScrapperFactory


CONFIG_PATH = 'config'
OUTPUT_PATH = 'output'
scrapper    = ScrapperFactory.productSearchResult()


def save(products):
    ut.save_json(f'{OUTPUT_PATH}/product_search_results_output', {'products': products})


with open(f'{CONFIG_PATH}/product_search_results_urls','r') as urls:
    products = []
    for url in urls.read().splitlines():
        results = scrapper.scrape(url)
        if results:
            for product in results['products']:
                logging.info("Saving Product: %s"%product['title'])
                products.append(product)
        ut.wait()
    save(products)