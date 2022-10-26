from utils import catch, remove_duplicate
import json
import urllib.parse

BASE_URL = 'https://www.amazon.com'


class ProductSearchTransform:
    def __init__(self, data):
        self.data = data

    def id(self):
        def transform(data):
            if 'products' in data:
                products = data['products']
                for p in products:
                    p['id'] = urllib.parse.unquote(p["url"]).split('/dp/')[1].split('/')[0]
        catch(transform, self.data, 'Error when extract id from url')
        return self

    def url(self):
        def transform(data):
            if 'products' in data:
                products = data['products']
                for p in products:
                    p['url'] = f'{BASE_URL}{urllib.parse.unquote(p["url"])}'
        catch(transform, self.data, 'Error when complete product url')
        return self

    def rating(self):
        def transform(data):
            data['rating']  = float(data['rating'].split('out of 5 stars')[0])
        catch(transform, self.data, 'Error when transform rating')
        return self

    def price(self):
        def transform(data):
            data['price']  = float(data['price'].replace('$', ''))
        catch(transform, self.data, 'Error when transform price')
        return self

    def get(self): return self.data