from selectorlib import Extractor
import requests 
import json 
import random
from time import sleep
from fake_useragent import UserAgent


exist_field = lambda field: lambda data: field not in data or data[field] == None


class Scrapper:
    def __init__(
        self,
        selector_file,
        proxy       = "http://40.129.203.4:8080",
        headers = {
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://www.amazon.com/',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'        }
    ):
        self.headers     = headers
        self.extractor   = Extractor.from_yaml_file(selector_file)
        self.user_agent  = UserAgent()
        self.proxies     = { "https": proxy}
        

    def scrape(
        self, 
        url, 
        retry_condition_fn = lambda data: False, 
        retry_multiplier   = 3,
        max_retry          = 10, 
        retry_start_time   = 2,
        max_retry_time     = 500
    ):
        retry_count = 1
        retry_time = retry_start_time
        while retry_count <= max_retry:
                self.headers['user-agent'] = self.user_agent.random

                # Download the page using requests
                print(f'Downloading {url}') 
                r = requests.get(url, headers=self.headers) #, proxies=self.proxies)

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
                    print(f'Retry({retry_count}) get {url} product detail after {retry_time} seconds...')
                    sleep(retry_time)
                    retry_time *= retry_multiplier
                    if retry_time > max_retry_time:
                        retry_time = max_retry_time
                    retry_count += 1
                else:
                    return data