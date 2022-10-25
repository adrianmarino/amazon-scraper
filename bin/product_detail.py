#/bin/python
import sys
sys.path.append('./src')
import logging
import utils as ut
from scrapper import ScrapperFactory
from save import save_json_html 


CONFIG_PATH = 'config'
logging.basicConfig(level=logging.INFO)


with open(f'{CONFIG_PATH}/product_detail_urls','r') as urls:
    for url in urls.read().splitlines():
        scrapper = ScrapperFactory.productDetail()

        result   = scrapper.scrape(url)
        if result.empty():
            continue

        if 'variants' in result.json[0] and result.json[0]['variants']:
            for variant in result.json[0]['variants']:
                variant_result = scrapper.scrape(variant['url'])
                save_detail_json_html(variant['id'], variant_result, variant=True)
        else:
            product_id = url.split('/')[-1]
            save_detail_json_html(product_id, result)

        if len(url) > 1:
            ut.wait()

