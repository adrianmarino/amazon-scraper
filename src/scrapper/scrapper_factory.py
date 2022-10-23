import logging
from .scrapper import Scrapper
from .transform import Transform

CONFIG_PATH = 'config'
PROXIES     =   {
                    'http':  'http://45.79.110.81:80',
                    'https': 'http://170.39.193.236:3128'
                }

class ScrapperFactory:
    @staticmethod
    def productSearchResult():
        return Scrapper(
            selector_file = f'{CONFIG_PATH}/product_search_results_selectors.yml',
            transform_fn  = lambda data: Transform(data).rating().data,
            proxies       = PROXIES
        )

    @staticmethod
    def productDetail():
        return Scrapper(
            selector_file = f'{CONFIG_PATH}/product_detail_selectors.yml',
            transform_fn  = lambda data: Transform(data).images().rating().price().reviews().data,
            proxies       = PROXIES
        )
