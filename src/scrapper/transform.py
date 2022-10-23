from utils import catch, remove_duplicate
import json


BASE_URL = 'https://www.amazon.com'


class Transform:
    def __init__(self, data):
        self.data = data

    def url(self):
        def transform(data):
            if 'products' in data:
                products = data['products']
                for p in products:
                    p['url'] = f'{BASE_URL}{p["url"]}'
        catch(transform, self.data, 'Error when complete product url')
        return self

    def variants(self):
        def transform(data):
            if 'variants' in data and type(data['variants']) == list:
                for v in data['variants']:
                    v['url'] = f'{BASE_URL}{v["url"]}'
        catch(transform, self.data, 'Error when transform product variants')
        return self

    def images(self):
        def transform(data):
            data['images']  = list(json.loads(data['images']).keys()), 
        catch(transform, self.data, 'Error when transform images')
        return self

    def rating(self):
        def transform(data):
            data['rating']  = float(data['rating'].split('out of 5 stars')[0])
        catch(transform, self.data, 'Error when transform rating')
        return self

    def price_range(self):
        def transform(data):
            prices = data['price_range'].split('P.when')[0].replace('Price:', '').replace('$', '').strip()
            prices = remove_duplicate(prices).split('-') 
            data['price_range']  = { 'from': float(prices[0].strip()), 'to': float(prices[1].strip()) }
        catch(transform, self.data, 'Error when transform price_range')
        return self


    def price(self):
        def transform(data):
            data['price']  = float(data['price'].replace('$', ''))
        catch(transform, self.data, 'Error when transform price')
        return self

    def reviews(self):
        def transform(data):
            data['reviews'] = int(data['reviews'].split('ratings')[0].strip().replace(',', ''))
        catch(transform, self.data, 'Error when transform reviews')
        return self

    def get(self): return self.data