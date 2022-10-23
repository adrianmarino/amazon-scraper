import logging
from .scrapper import Scrapper
from .transform import Transform

CONFIG_PATH = 'config'

class ScrapperFactory:
    @staticmethod
    def productSearchResult():
        return Scrapper(
            selector_file = f'{CONFIG_PATH}/search_results_selectors.yml',
            transform_fn  = lambda data: Transform(data).rating().data
        )

    @staticmethod
    def productDetail():
        return Scrapper(
            selector_file = f'{CONFIG_PATH}/product_detail_selectors.yml',
            transform_fn  = lambda data: Transform(data).images().rating().price().reviews().data
        )
