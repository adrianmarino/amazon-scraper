from utils import catch
import json


class Transform:
    def __init__(self, data):
        self.data = data

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