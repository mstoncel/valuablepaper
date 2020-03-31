from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from app.api.models import Stock
from app.provider.models import Provider
from app.api.views import StockView
from rest_framework.test import APIClient


class TestCase(TestCase):
    def setUp(self):
        stock_data = {
            'symbol': 'ISDMR',
            'real_price': 10.0,
            'start_price': 8.0,
            'title': 'Iskenderun Demir Çelik',
            'provider_id': 1
        }
        provider_data = {
            'name': 'bigpara',
            'status': 'active',
            'data': {
                "base_url": "http://bigpara.hurriyet.com.tr/borsa/hisse-fiyatlari/"
            }
        }

        self.client = APIClient()
        self.provider = Provider.objects.create(**provider_data)
        self.stock = Stock.objects.create(**stock_data)
        self.stock_url = reverse('stock:single_stock', args=[self.stock.symbol])

    def test_check_symbol_stock_GET(self):
        response = self.client.get(self.stock_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

