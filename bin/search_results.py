import sys
sys.path.append('./src')


from time import sleep
import json
import random
import logging
from scrapper import ProductSearchResultScrapper

CONFIG_PATH = 'config'
OUTPUT_PATH = 'output'
scrapper    = ProductSearchResultScrapper(f'{OUTPUT_PATH}/search_results_selectors.yml')
DELAYS      = list(range(1, 5))

# product_data = []
with open(f'{CONFIG_PATH}/search_results_urls','r') as urls, open(f'{CONFIG_PATH}/search_results_output.json','w') as outfile:
    products = []

    for url in urls.read().splitlines():
        results = scrapper.scrape(url)
        if results:
            for product in results['products']:
                print("Saving Product: %s"%product['title'])
                products.append(product)

        delay = random.choice(DELAYS)
        print(f'Wait {delay} seconds...')

    outfile.write(json.dumps({'products': products}, indent=2))