import re
from bs4 import BeautifulSoup


class Adapter(object):

    def __init__(self, *args, **kwargs):
        self.provider = kwargs.get('provider')
        self.client = self.provider.get_client(**self.provider.data)

    def validation_response(self, soup, stock_symbol):
        check_symbol = soup.find('a', class_='active').text
        if not stock_symbol.upper() == check_symbol.upper():
            return {'error': True}
        return {'error': False}

    def initial_stock_data(self, stock_symbol):
        response = self.client.extract_stock(stock_symbol)
        if not response.ok:
            return {}
        soup = BeautifulSoup(response.content, 'lxml')
        valid_data = self.validation_response(soup, stock_symbol)
        if valid_data.get('error'):
            return {}
        real_price = soup.select_one(
            '''div.realTime > span.price-arrow-down,
             div.realTime > span.price-arrow-up''').text
        last_price = soup.select_one(
            ' div.realTime > table > tbody > tr.last > td:nth-child(2)').text
        start_price = \
            re.findall(r"[-+]?\d*\.\d+|\d+", last_price.replace(',', '.'))[0]
        real_price = real_price.replace(',', '.')
        stock_data = dict(
            symbol=stock_symbol.upper(),
            real_price=float(real_price),
            start_price=float(start_price),
            provider_name=self.provider.name,
        )
        return stock_data
