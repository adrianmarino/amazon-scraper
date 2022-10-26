import logging
import utils as ut


BASE_URL    = 'https://www.amazon.com/'
OUTPUT_PATH = 'output'


def save_html(url, content):
    url = url.replace(BASE_URL, '')
    with open(f'{OUTPUT_PATH}/{url}.html', 'w') as f: f.write(content)


def save_detail_json_html(product_id, result, variant_id=None):
    filename = f'{product_id}_variant_{variant_id}' if variant_id else product_id

    logging.info(f'Save {filename} product...')    
    ut.save_json(f'{OUTPUT_PATH}/{filename}', result.json[0])
    with open(f'{OUTPUT_PATH}/{filename}.html', 'w') as f: f.write(result.html)

def save_json_search_result(products):
    ut.save_json(f'{OUTPUT_PATH}/product_search_results_output', {'products': products})


def save_reviews(product_id, reviews):
    logging.info(f'Save {product_id} reviews...')
    ut.save_json(f'{OUTPUT_PATH}/{product_id}_reviews', reviews)