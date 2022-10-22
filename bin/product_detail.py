import sys
sys.path.append('./src')

import json 
from time import sleep
import random 
import logging
from scrapper import exist_field, ProductDetailScrapper


BASE_URL    = 'https://www.amazon.com'
CONFIG_PATH = 'config'
OUTPUT_PATH = 'output'
scrapper    = ProductDetailScrapper(f'{CONFIG_PATH}/product_detail_selectors.yml')
DELAYS      = list(range(1, 5))


def save_as_json(path, data):
    with open(f'{path}.json', 'w') as outfile:
        outfile.write(json.dumps(data, indent=2))

# product_data = []
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
                    save_as_json(f'{OUTPUT_PATH}/{variant["id"]}', variant_detail)
            else:
                product_id = url.split('/')[-1]
                logging.info(f'Add {product_id} root product...')
                save_as_json(f'{OUTPUT_PATH}/{product_id}', detail)

        delay = random.choice(DELAYS)
        logging.info(f'Wait {delay} seconds...')
        if len(url) > 1:
            sleep(delay)
