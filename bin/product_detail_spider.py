#/bin/python

import sys
sys.path.append('./src')

import json
from time import sleep
import random 
import logging
import utils as ut
from scrapper import ScrapperFactory


BASE_URL        = 'https://www.amazon.com'
CONFIG_PATH     = 'config'
OUTPUT_PATH     = 'output'
detail_scrapper = ScrapperFactory.productDetail()
result_scrapper = ScrapperFactory.productSearchResult()
logging.basicConfig(level=logging.INFO)


def save(product_id, result, variant=False):
    logging.info(f'Save {product_id}(variante:{variant}) product...')    
    filename = f'{product_id}{"_variant" if variant else ""}'
    ut.save_json(f'{OUTPUT_PATH}/{filename}', result.json[0])
    with open(f'{OUTPUT_PATH}/{filename}.html', 'w') as f: f.write(result.html)


def retry_cond(data): return not 'description' in data


def save_html(url, content):
    url = url.replace(BASE_URL, '')
    with open(f'{OUTPUT_PATH}/{url}.html', 'w') as f: f.write(content)


with open(f'{CONFIG_PATH}/product_search_results_urls', 'r') as urls:
    for url in urls.read().splitlines():
        search_result = result_scrapper.scrape(url)
        if not search_result.empty():
            save_html(url, search_result.html)

            for product in search_result.json[0]['products']:
                
                detail_result = detail_scrapper.scrape(product['url'], retry_condition_fn=retry_cond)

                print('detail_result:', detail_result.json)

                if not detail_result.empty():
                    if 'variants' in detail_result.json[0] and detail_result.json[0]['variants']:
                        for variant in detail_result.json[0]['variants']:
                            variant_result = detail_scrapper.scrape(variant['url'], retry_condition_fn=retry_cond)
                            save(variant['id'], variant_result, variant=True)
                    else:
                        print(detail_result.json[0])
                        product_id = detail_result.json[0]['id']
                        save(product_id, detail_result)

        if len(url) > 1:
            ut.wait()

