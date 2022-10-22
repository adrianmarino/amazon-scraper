import logging
from .scrapper import Scrapper


class ProductSearchResultScrapper(Scrapper):
    def __init__(self, selector_file): super().__init__(selector_file)
    def scrape(self, url):
        detail = super().scrape(url)
        if detail == None:
            return detail

        try:
            detail['rating']  = float(detail['rating'].split('out of 5 stars')[0])
        except:
            logging.warn('rating transform error')

        try:
            detail['price']  = float(detail['price'].replace('$', ''))
        except:
            logging.warn('rating transform error')

        try:
            detail['reviews'] = int(detail['reviews'].split('ratings')[0].strip().replace(',', ''))
        except:
            logging.warn('reviews transform error')

        return detail