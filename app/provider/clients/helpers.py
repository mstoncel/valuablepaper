import re
import unicodedata


def convert_float(price):
    return float(price.replace(',', '.'))


def find_float(data):
    normalize_data = unicodedata.normalize('NFKD', data)
    extract_price = float(
        re.findall(r"[-+]?\d*\.\d+|\d+", normalize_data.replace(',', '.'))[0])
    return extract_price
