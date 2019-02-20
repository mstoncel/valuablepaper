from bs4 import BeautifulSoup
from app.provider.clients.helpers import find_float

from app.api.models import Stock


class Adapter:

    def __init__(self, *args, **kwargs):
        self.provider = kwargs.get('provider')
        self.client = self.provider.get_client(**self.provider.data)

    def validation_response(self, soup, stock_symbol):
        stock = soup.select_one(
            '''#content > div.wideContent.clearfix > 
            ul > li:nth-child(4) > a > span''')
        if not stock or not stock_symbol.upper() == stock.text.upper():
            return {'error': True}
        return {'error': False}

    def initial_stock_data(self, stock_symbol):
        response = self.client.extract_stock(stock_symbol.lower())
        soup = BeautifulSoup(response.content, 'lxml')
        validate_data = self.validation_response(soup, stock_symbol)
        if validate_data.get('error'):
            return {}
        start_price = soup.select_one('''
            #content > div.contentLeft > div.otyTable1.mBot20 > div.otyBody > 
            div:nth-child(3) > span:nth-child(1)''').text
        start_price = float(start_price.replace(',', '.'))
        last_price = soup.select_one(
            '''#content > div.contentLeft > div.hisseProcessBar.mBot10 > 
            text > ul > li.type.up > span''').text
        last_price = float(last_price.replace(',', '.'))
        stock_data = dict(
            symbol=stock_symbol.upper(),
            provider_name=self.provider.name,
            real_price=last_price,
            start_price=start_price
        )
        return stock_data

    def initial_all_stock_data(self):
        stock_data = []
        response = self.client.extract_all_stock()
        soup = BeautifulSoup(response.content, 'lxml')
        links = soup.find('div', class_='sortOfBar').select('a')
        for link in links:
            results = self.client.stock_table_data(link.get('href'))
            soup = BeautifulSoup(results.content, 'lxml')
            data_response = soup.select(
                """#content > div.contentLeft > div.tableCnt > 
                div > div > div.tBody > ul""")
            for data in data_response:
                symbol = data.select_one('li:nth-of-type(1)').text
                real_price = find_float(
                    data.select_one('li:nth-of-type(2)').text)
                start_price = find_float(
                    data.select_one('li:nth-of-type(3)').text)
                data = dict(
                    symbol=symbol,
                    real_price=real_price,
                    start_price=start_price,
                    provider=self.provider

                )
                stock_data.append(Stock(**data))
        return stock_data
