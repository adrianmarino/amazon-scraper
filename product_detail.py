import json 
from time import sleep
from scrapper import Scrapper
import random 

class ProductDetailScrapper(Scrapper):
    def __init__(self, selector_file): super().__init__(selector_file)
    def scrape(self, url, retry=10):
        retry_time = 1
        while retry_time <= retry:
            detail = super().scrape(url)
            if 'description' in detail and detail['description'] != None:
                detail['images']  = list(json.loads(detail['images']).keys())
                detail['rating']  = float(detail['rating'].split('out of 5 stars')[0])
                detail['reviews'] = int(detail['reviews'].split('ratings')[0].strip().replace(',', ''))
                return detail
            else:
                product_id = url.split('/')[-1]
                print(f'Retry get {product_id} product detail after {retry_time} seconds...')
                sleep(retry_time)
                retry_time *= 2

BASE_URL='https://www.amazon.com'

scrapper = ProductDetailScrapper('product_detail_selectors.yml')

DELAYS = list(range(1, 5))

# product_data = []
with open("product_detail_urls.txt",'r') as urls, open('product_details.json','w') as outfile:
    details = []
    for url in urls.read().splitlines():
        detail = scrapper.scrape(url)
        if detail:
            if 'variants' in detail:
                for variant in [detail['variants'][0]]:
                    variant_detail = scrapper.scrape(f'{BASE_URL}{variant["url"]}')
                    print(f'Add {variant["id"]} variant product...')
                    del variant_detail['variants']
                    details.append(variant_detail)
            else:
                product_id = url.split('/')[-1]
                print(f'Add {product_id} root product...')
                details.append(detail)
        
        delay = random.choice(DELAYS)
        print(f'Wait {delay} seconds...')
        sleep(delay)

    outfile.write(json.dumps({'products': details}, indent=2))

