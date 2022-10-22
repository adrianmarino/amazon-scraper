import json 
from time import sleep
from scrapper import Scrapper
import random 

class ProductDetailScrapper(Scrapper):
    def __init__(self, selector_file): super().__init__(selector_file)
    def scrape(self, url):
        detail = super().scrape(
            url, 
            retry_condition_fn=lambda data: 'description' not in data or data['description'] == None
        )
        if detail == None:
            return detail

        if 'images' in detail:
            detail['images']  = list(json.loads(detail['images']).keys())

        if 'rating' in detail:
            detail['rating']  = float(detail['rating'].split('out of 5 stars')[0])

        if 'price' in detail:
            detail['price']  = float(detail['price'].replace('$', ''))

        if 'reviews' in detail:
            detail['reviews'] = int(detail['reviews'].split('ratings')[0].strip().replace(',', ''))

        if 'extra_detail' in detail:
            for item in detail['extra_detail']:
                item['field'] = item['field'].split('\n')[0].strip()
                item['value'] = item['value'].split('\n')[0].strip()

        return detail


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

        if len(url) > 1:
            sleep(delay)

    outfile.write(json.dumps({'products': details}, indent=2))

