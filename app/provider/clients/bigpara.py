import os
import requests
import json


class Client:
    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.get('base_url')

    def make_request(self, url, method='get', post_data=None):
        if method.lower() in ('get', 'delete'):
            post_data = {}
        url = os.path.join(self.base_url, url)
        return requests.request(method=method, url=url,
                                data=json.dumps(post_data))

    def extract_stock(self, stock_symbol):
        url = '{}-detay/teknik-yorum/'.format(stock_symbol)
        return self.make_request(url=url)

    def extract_all_stock(self):
        return self.make_request(url='')

    def stock_table_data(self, link):
        url = [item for item in link.split('/') if item != ''][-1]
        return self.make_request(url=url)
