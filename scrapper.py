from selectorlib import Extractor
import requests 
import json 
import random
from time import sleep


class Scrapper:
    def __init__(
        self,
        selector_file,
        user_agents = [ 
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Chrome/51.0.2704.103',
            'Safari/537.36',
            'Opera/9.80 (Macintosh; Intel Mac OS X; U; en) Presto/2.2.15 Version/10.00'
            'Opera/9.60 (Windows NT 6.0; U; en) Presto/2.1.1'
            'Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
        ],
        headers = {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.amazon.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
    ):
        self.user_agents = user_agents
        self.headers     = headers
        self.extractor   = Extractor.from_yaml_file(selector_file)

    def scrape(self, url, retry_condition_fn=lambda data: False, retry=10):
        retry_time = 1
        while retry_time <= retry:
                self.headers['user-agent'] = random.choice(self.user_agents)

                # print('Headers:', json.dumps(self.headers, indent=2))

                # Download the page using requests
                print("Downloading %s"%url)
                r = requests.get(url, headers=self.headers)

                # Simple check to check if page was blocked (Usually 503)
                if r.status_code > 500:
                    if "To discuss automated access to Amazon data please contact" in r.text:
                        print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
                    else:
                        print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
                    return None

                # Pass the HTML of the page and create 
                data = self.extractor.extract(r.text)

                if retry_condition_fn(data):
                    product_id = url.split('/')[-1]
                    print(f'Retry get {product_id} product detail after {retry_time} seconds...')
                    sleep(retry_time)
                    retry_time *= 2
                else:
                    return data
