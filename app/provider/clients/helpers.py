import re
import unicodedata
from functools import wraps
from urllib3 import exceptions
from requests import exceptions as requests_exceptions
from app.api.datastructures import ResponsePayload


class ProviderClientError(Exception):

    def __init__(self, http_status, detail):
        super(Exception, self).__init__(detail)
        self.http_status = http_status


def convert_float(price: str) -> float:
    return float(price.replace(',', '.'))


def find_float(data: str) -> float:
    normalize_data = unicodedata.normalize('NFKD', data)
    extract_price = float(
        re.findall(r"[-+]?\d*\.\d+|\d+", normalize_data.replace(',', '.'))[0])
    return extract_price


def client_response_validation(func_name):
    @wraps(func_name)
    def wrapper(*args, **kwargs):
        try:
            response = func_name(*args, **kwargs)
            if response.ok:
                response = ResponsePayload(error=False,
                                           results=response.content)
            else:
                response = ResponsePayload(error=True, results=[])

        except (exceptions.ReadTimeoutError,
                requests_exceptions.ReadTimeout,
                exceptions.ConnectionError,
                requests_exceptions.ConnectionError) as e:
            response = ResponsePayload(error=True, results=[])
        finally:
            return response
    return wrapper
