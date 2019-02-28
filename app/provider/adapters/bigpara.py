from bs4 import BeautifulSoup
from app.api.datastructures import ResponseError
from app.provider.clients.helpers import find_float, convert_float
from app.api.models import Stock
from tqdm import tqdm


class Adapter:

    def __init__(self, *args, **kwargs):
        self.provider = kwargs.get('provider')
        self.client = self.provider.get_client(**self.provider.data)

    def soup_generator(self, response, stock_symbol=None):
        soup = BeautifulSoup(response, 'lxml')
        if stock_symbol:
            validate_soup = self.validation_response(soup, stock_symbol)
            if validate_soup.error:
                return validate_soup
        return soup

    def validation_response(self, soup: BeautifulSoup,
                            stock_symbol: str) -> ResponseError:
        stock = soup.select_one(
            '''#content > div.wideContent.clearfix > 
            ul > li:nth-child(4) > a > span''')
        if not stock or not stock_symbol.upper() == stock.text.upper():
            return ResponseError(error=True)
        return ResponseError(error=False)

    def initial_stock_data(self, stock_symbol):
        response = self.client.extract_stock(stock_symbol.lower())
        stock_data = {}
        if not response.error or response:
            soup = self.soup_generator(response.results, stock_symbol)
            if soup.error:
                return stock_data
            start_price = soup.select_one('''
                #content > div.contentLeft > div.otyTable1.mBot20 > 
                div.otyBody > div:nth-child(3) > span:nth-child(1)''').text
            start_price = convert_float(start_price)
            last_price = soup.select_one('#content > div.contentLeft > '
                                         'div.hisseProcessBar.mBot10 > text >'
                                         ' ul > li.type.up > span , #content >'
                                         ' div.contentLeft > '
                                         'div.hisseProcessBar.mBot10 > text '
                                         '> ul > li.type.dw > span').text
            last_price = convert_float(last_price)
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
        if not response.error:
            soup = self.soup_generator(response.results)
            if soup.error:
                return {}
            links = soup.find('div', class_='sortOfBar').select('a')
            for link in tqdm(links):
                response_ = self.client.stock_table_data(link.get('href'))
                if response_.error:
                    continue
                soup = self.soup_generator(response_.results)
                data_response = soup.select(
                    """#content > div.contentLeft > div.tableCnt > 
                    div > div > div.tBody > ul""")
                for data in data_response:
                    symbol = data.select_one('li:nth-of-type(1)').text
                    real_price = find_float(
                        data.select_one('li:nth-of-type(2)').text)
                    start_price = find_float(
                        data.select_one('li:nth-of-type(3)').text)
                    title_html = self.client.extract_stock(symbol)
                    if not title_html.results:
                        continue
                    soup = self.soup_generator(title_html.results)
                    title = soup.select_one(
                        '#content > div.contentLeft > h1').text.strip()
                    data = dict(
                        symbol=symbol,
                        real_price=real_price,
                        start_price=start_price,
                        provider=self.provider,
                        title=title

                    )
                    stock_data.append(Stock(**data))

        return stock_data
