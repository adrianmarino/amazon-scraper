#/bin/python
import sys
sys.path.append('./src')
import logging
import utils as ut
from scrapper import ScrapperFactory
from save import save_json_html, save_html


CONFIG_PATH     = 'config'
logging.basicConfig(level=logging.INFO)


with open(f'{CONFIG_PATH}/product_search_results_urls', 'r') as urls:
    for url in urls.read().splitlines():
        result_scrapper = ScrapperFactory.productSearchResult()
        detail_scrapper = ScrapperFactory.productDetail()

        search_result = result_scrapper.scrape(url)
        if not search_result.empty():
            save_html(url, search_result.html)

            for product in search_result.json[0]['products']:                
                detail_result = detail_scrapper.scrape(product['url'])

                if not detail_result.empty():
                    if 'variants' in detail_result.json[0] and detail_result.json[0]['variants']:
                        for variant in detail_result.json[0]['variants']:
                            variant_result = detail_scrapper.scrape(variant['url'])
                            save_json_html(variant['id'], variant_result, variant=True)
                    else:
                        product_id = detail_result.json[0]['id']
                        save_json_html(product_id, detail_result)

        if len(url) > 1:
            ut.wait()
