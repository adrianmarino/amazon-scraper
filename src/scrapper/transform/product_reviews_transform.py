from utils import catch, remove_duplicate
import json


BASE_URL = 'https://www.amazon.com'


class ProductReviewsTransform:
    def __init__(self, data):
        self.data = data

    def rating(self):
        def transform(data):
            for review in data['reviews']:
                review['rating'] = float(review['rating'].split('out of 5 stars')[0])
        catch(transform, self.data, 'Error when transform rating')
        return self

    def next_page(self):
        def transform(data):
            data['next_page'] = f'{BASE_URL}{data["next_page"]}' 
        catch(transform, self.data, 'Error when transform next page')
        return self

    def get(self): return self.data