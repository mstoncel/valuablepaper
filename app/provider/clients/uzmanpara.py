import os
import json
import requests
import logging

logger = logging.getLogger('main')


class Client(object):

    def __init__(self, *args, **kwargs):
        self.base_url = kwargs.get('base_url')

    def make_request(self, request_url, method='get', post_data=None):
        if method.lower() not in ('get', 'delete'):
            post_data = {}
        return requests.request(method=method, url=request_url,
                                data=json.dumps(post_data))

    def extract_stock(self, stock_symbol):
        stock_url = os.path.join(self.base_url, stock_symbol.upper())
        return self.make_request(request_url=stock_url)
