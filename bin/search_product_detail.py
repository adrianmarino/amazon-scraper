import sys
sys.path.append('./src')

import json
from time import sleep
import random 
import logging
import utils as ut
from scrapper import exist_field, ProductDetailScrapper, ProductSearchResultScrapper


BASE_URL        = 'https://www.amazon.com'
CONFIG_PATH     = 'config'
OUTPUT_PATH     = 'output'
detail_scrapper = ProductDetailScrapper(f'{CONFIG_PATH}/product_detail_selectors.yml')
result_scrapper = ProductSearchResultScrapper(f'{CONFIG_PATH}/search_results_selectors.yml')
DELAYS          = list(range(1, 5))


with open(f'{CONFIG_PATH}/search_results_urls', 'r') as urls:
    for url in urls.read().splitlines():
        results = result_scrapper.scrape(url)

        if results:
            for product in results['products']:
                detail_url = f'{BASE_URL}{product["url"]}'
                detail = detail_scrapper.scrape(detail_url)
                if detail_url:
                    if 'variants' in detail:
                        if detail['variants']:
                            for variant in detail['variants']:
                                variant_detail = detail_scrapper.scrape(f'{BASE_URL}{variant["url"]}')
                                print(f'Save {variant["id"]} variant product...')
                                del variant_detail['variants']
                                ut.save_json(f'{OUTPUT_PATH}/{variant["id"]}', variant_detail)
                    else:
                        print(f'Save {detail["id"]} root product...')
                        ut.save_json(f'{OUTPUT_PATH}/{detail["id"]}', detail)

        delay = random.choice(DELAYS)
        print(f'Wait {delay} seconds...')
        if len(url) > 1:
            sleep(delay)

