#/bin/python

import sys
sys.path.append('./src')

import json 
from time import sleep
import random 
import logging
import utils as ut
from scrapper import ScrapperFactory


CONFIG_PATH = 'config'
OUTPUT_PATH = 'output'
scrapper    = ScrapperFactory.productDetail()
logging.basicConfig(level=logging.INFO)


def save(product_id, result, variant=False):
    logging.info(f'Save {product_id}(variante:{variant}) product...')    
    filename = f'{product_id}{"_variant" if variant else ""}'
    ut.save_json(f'{OUTPUT_PATH}/{filename}', result.json[0])
    with open(f'{OUTPUT_PATH}/{filename}.html', 'w') as f: f.write(result.html)


def retry_cond(data): return not 'description' in data


with open(f'{CONFIG_PATH}/product_detail_urls','r') as urls:
    for url in urls.read().splitlines():
        result = scrapper.scrape(url, retry_condition_fn=retry_cond)
        if result.empty():
            continue

        if 'variants' in result.json[0] and result.json[0]['variants']:
            for variant in result.json[0]['variants']:
                variant_result = scrapper.scrape(variant['url'], retry_condition_fn=retry_cond)
                save(variant['id'], variant_result, variant=True)
        else:
            product_id = url.split('/')[-1]
            save(product_id, result)

        if len(url) > 1:
            ut.wait()

