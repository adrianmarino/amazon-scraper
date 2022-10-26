#/bin/python
import sys
sys.path.append('./src')
import utils as ut
from scrapper import ScrapperFactory
from save import save_reviews 
import logging
import glob
import json


CONFIG_PATH = 'config'
logging.basicConfig(level=logging.INFO)
MAX_PAGES = 10


product_detail_paths = glob.glob("output/*_reviews.json")
processed_products = [p.split('/')[1].split('_reviews.json')[0] for p in product_detail_paths]
print('Already processes products:', processed_products)

for product_detail_path in glob.glob("output/*.json"):
    if 'reviews' in product_detail_path or 'search_results' in product_detail_path:
        continue

    with open(product_detail_path,'r') as f:
        product_detail = json.load(f)

    if product_detail['id'] in processed_products:
        logging.info(f'{product_detail["id"]} already processes')
        continue

    reviews = []
    scrapper = ScrapperFactory.productReviews()
 
    if product_detail['reviews_link'] is None or product_detail['reviews_link'] == 'https://www.amazon.comNone':
        continue
 
    result = scrapper.scrape(product_detail['reviews_link'])
    pages_count = 0 
    while not result.empty() and pages_count < MAX_PAGES:
        if result.json[0]['reviews']:
            reviews.extend(result.json[0]['reviews'])
        
        if 'next_page' in result.json[0]:
            if result.json[0]['next_page'] == 'https://www.amazon.comNone':
                break

            ut.wait()
            result = scrapper.scrape(result.json[0]['next_page'])
            pages_count += 1
        else:
            break

    processed_products.append(product_detail['id'])
    save_reviews(product_detail['id'], reviews)


