#/bin/python
import sys
sys.path.append('./src')
import logging
import utils as ut
from scrapper import ScrapperFactory
from save import save_reviews 
import logging


CONFIG_PATH = 'config'
logging.basicConfig(level=logging.INFO)
MAX_PAGES = 10

with open(f'{CONFIG_PATH}/product_reviews_urls','r') as urls:
    reviews = []
    
    for url in urls.read().splitlines():
        product_id = url.split('product-reviews/')[1].split('/')[0]
        
        result   = scrapScrapperFactory.productReviews().scrape(url)

        pages_count = 0 
        while not result.empty() and pages_count < MAX_PAGES:
            reviews.extend(result.json[0]['reviews'])
            
            if 'next_page' in result.json[0]:
               ut.wait()
               result = ScrapperFactory.productReviews().scrape(result.json[0]['next_page'])
               pages_count += 1
            else:
                break

        save_reviews(product_id, reviews)