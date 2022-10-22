import json
import logging
from .scrapper import Scrapper


class ProductDetailScrapper(Scrapper):
    def __init__(self, selector_file): super().__init__(selector_file)
    def scrape(self, url):
        detail = super().scrape(url)
        if detail == None:
            return detail

        try:
            detail['images']  = list(json.loads(detail['images']).keys())
        except Exception as e:
            logging.warning(f'Error when transform images. Detail: {e}')

        try:
            detail['rating']  = float(detail['rating'].split('out of 5 stars')[0])
        except Exception as e:
            logging.warning(f'Error when transform rating. Detail: {e}')

        # try:
        #    detail['price']  = float(detail['price'].replace('$', ''))
        #except Exception as e:
        #    logging.warning(f'Error when transform price. Detail: {e}')

        try:
            detail['reviews'] = int(detail['reviews'].split('ratings')[0].strip().replace(',', ''))
        except Exception as e:
            logging.warning(f'Error when transform reviews. Detail: {e}')

        return detail