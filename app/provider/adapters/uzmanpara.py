import re
from bs4 import BeautifulSoup
from app.api.datastructures import ResponseError


class Adapter:

    def __init__(self, *args, **kwargs):
        self.provider = kwargs.get('provider')
        self.client = self.provider.get_client(**self.provider.data)

    def soup_generator(self, response, stock_symbol):
        soup = BeautifulSoup(response, 'lxml')
        if stock_symbol:
            validate_ = self.validation_response(soup, stock_symbol)
            if validate_.error:
                return validate_
        return soup

    def validation_response(self, soup, stock_symbol):
        check_symbol = soup.find('a', class_='active').text
        if not stock_symbol.upper() == check_symbol.upper():
            return ResponseError(error=True)
        return ResponseError(error=False)

    def initial_stock_data(self, stock_symbol):
        response = self.client.extract_stock(stock_symbol)
        stock_data = {}
        if response.results:
            soup = self.soup_generator(response.results, stock_symbol)
            if soup.error:
                return stock_data
            real_price = soup.select_one(
                '''div.realTime > span.price-arrow-down,
                 div.realTime > span.price-arrow-up''').text
            last_price = soup.select_one(
                """div.realTime > table > tbody > tr.last > 
                        td:nth-child(2)""").text
            start_price = \
                re.findall(r"[-+]?\d*\.\d+|\d+", last_price.replace(',', '.'))[
                    0]
            real_price = real_price.replace(',', '.')
            stock_data = dict(
                symbol=stock_symbol.upper(),
                real_price=float(real_price),
                start_price=float(start_price),
                provider_name=self.provider.name,
            )
        return stock_data

    def initial_all_stock_data(self):
        return []
