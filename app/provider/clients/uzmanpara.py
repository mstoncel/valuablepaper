import os
import json
import requests
import logging

logger = logging.getLogger('main')


class Client:

    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.get('base_url')

    def make_request(self, url, method='get', post_data=None):
        if method.lower() not in ('get', 'delete'):
            post_data = {}
        url = os.path.join(self.base_url, url)
        return requests.request(method=method, url=url,
                                data=json.dumps(post_data))

    def extract_stock(self, stock_symbol):
        url = os.path.join('borsa/hisse-senetleri', stock_symbol.upper())
        return self.make_request(url=url)

    def extract_all_stock(self):
        url = 'canli-borsa/'
        return self.make_request(url=url)

    def stock_table_data(self, link):
        url = [item for item in link.split('/') if item != ''][-1]
        return self.make_request(url=url)



