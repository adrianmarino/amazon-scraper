import sys
sys.path.append('./src')

import json 
from time import sleep
import random 
import logging
import utils as ut
from scrapper import ScrapperFactory


BASE_URL    = 'https://www.amazon.com'
CONFIG_PATH = 'config'
OUTPUT_PATH = 'output'
scrapper    = ScrapperFactory.productDetail()


with open(f'{CONFIG_PATH}/product_detail_urls','r') as urls:
    details = []
    for url in urls.read().splitlines():
        detail = scrapper.scrape(url)
        if detail:
            if False and 'variants' in detail:
                for variant in detail['variants']:
                    variant_detail = scrapper.scrape(f'{BASE_URL}{variant["url"]}')
                    logging.info(f'Add {variant["id"]} variant product...')
                    del variant_detail['variants']
                    ut.save_json(f'{OUTPUT_PATH}/{variant["id"]}', variant_detail)
            else:
                product_id = url.split('/')[-1]
                logging.info(f'Add {product_id} root product...')
                ut.save_json(f'{OUTPUT_PATH}/{product_id}', detail)

        if len(url) > 1:
            ut.wait()

