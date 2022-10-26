import logging
from .scrapper import Scrapper
from .transform import   ProductDetailTransform, \
                        ProductSearchTransform, \
                        ProductReviewsTransform


CONFIG_PATH = 'config'
PROXIES     =   {
                    'http':  'http://38.94.109.12:80',
                    'https': 'http://35.131.26.94:3129'
                }

HEADERS     = {
    'Accept-Language'   : 'en-US,en;q=0.9',
    'Referer'           : 'https://www.amazon.com/',
    'sec-ch-ua'         : '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile'  : '?0',
    'sec-ch-ua-platform': "Linux",
    'Sec-Fetch-Dest'    : 'empty',
    'Sec-Fetch-Mode'    : 'cors',
    'Sec-Fetch-Site'    : 'same-site',
    'dnt': '1',
    'upgrade-insecure-requests': '1'         
}


class ScrapperFactory:
    @staticmethod
    def productSearchResult():
        return Scrapper(
            selector_file = f'{CONFIG_PATH}/product_search_results_selectors.yml',
            transform_fn  = lambda d: ProductSearchTransform(d).id().url().price().rating().get(),
            proxies       = PROXIES
        )

    @staticmethod
    def productDetail():
        return Scrapper(
            selector_file       = f'{CONFIG_PATH}/product_detail_selectors.yml',
            transform_fn        = lambda d: ProductDetailTransform(d) \
                .variants() \
                .images() \
                .rating() \
                .price_range() \
                .reviews_count() \
                .reviews_link() \
                .get(),
            headers             = HEADERS,
            proxies             = PROXIES,
            retry_condition_fn  = lambda data: not ('description' in data)
        )


    @staticmethod
    def productReviews():
        return Scrapper(
            selector_file       = f'{CONFIG_PATH}/product_reviews_selectors.yml',
            transform_fn        = lambda d: ProductReviewsTransform(d).rating().next_page().get(),
            headers             = HEADERS,
            proxies             = PROXIES
        )

