import re
import unicodedata
from functools import wraps

from app.api.datastructures import ResponsePayload


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
        response = func_name(*args, **kwargs)

        if response.ok:
            response = ResponsePayload(error=False, results=response.content)
        else:
            response = ResponsePayload(error=True, results=[])
        return response
    return wrapper
