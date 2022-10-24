#/bin/python
import sys
sys.path.append('./src')
import logging
import utils as ut
from scrapper import ScrapperFactory
from save import save_html, save_json_search_result


CONFIG_PATH = 'config'
logging.basicConfig(level=logging.INFO)


with open(f'{CONFIG_PATH}/product_search_results_urls','r') as urls:
    products = []
    for url in urls.read().splitlines():
        scrapper = ScrapperFactory.productSearchResult()
        result   = scrapper.scrape(url)
        if not result.empty():
            save_html(url, result.html)
            for product in result.json[0]['products']:
                logging.info("Product: %s"%product['title'])
                products.append(product)
        ut.wait()
    save_json_search_result(products)