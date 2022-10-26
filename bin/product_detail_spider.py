#/bin/python
import sys
sys.path.append('./src')
import logging
import utils as ut
from scrapper import ScrapperFactory
from save import save_detail_json_html, save_html
import glob


CONFIG_PATH     = 'config'
logging.basicConfig(level=logging.INFO)


product_detail_paths = glob.glob("output/*_variant_*.json")
processed_products = [p.split('/')[1].split('_variant_')[0].strip() for p in product_detail_paths]
processed_products.extend([p.split('/')[1].split('_variant_')[1].split('.json')[0].strip() for p in product_detail_paths])
processed_products = list(set(processed_products))
print('Already processes products:', len(processed_products))


with open(f'{CONFIG_PATH}/product_search_results_urls', 'r') as urls:
    for url in urls.read().splitlines():
        search_result = ScrapperFactory.productSearchResult().scrape(url)
        if not search_result.empty():
            for product in search_result.json[0]['products']:
                if product['id'] in processed_products:
                    logging.info(f'{product["id"]} already processes')
                    continue
                processed_products.append(product['id'])

                detail_result = ScrapperFactory.productDetail().scrape(product['url'])
                if not detail_result.empty():
                    if 'variants' in detail_result.json[0] and detail_result.json[0]['variants']:
                        for variant in detail_result.json[0]['variants']:
                            if variant['id'] in processed_products:
                                logging.info(f'{variant["id"]} variant already processes')
                                continue
                            variant_result = ScrapperFactory.productDetail().scrape(variant['url'])
                            save_detail_json_html(product['id'], variant_result, variant_id=variant['id'])
                            ut.wait()
                    else:
                        save_detail_json_html(product['id'], detail_result)
                        ut.wait()

            save_html(url, search_result.html)
