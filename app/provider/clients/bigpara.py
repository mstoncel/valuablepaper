import requests
import json


class Client:
    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.get('base_url')

    def make_request(self, url, method='get', post_data=None):
        if method.lower() in ('get', 'delete'):
            post_data = {}

        return requests.request(method=method, url=url,
                                data=json.dumps(post_data))

    def extract_stock(self, stock_symbol):
        base_url = self.base_url.format(stock_symbol)
        return self.make_request(url=base_url)
