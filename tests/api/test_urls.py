from django.test import TestCase
from django.urls import reverse, resolve, NoReverseMatch
from app.api.views import StockView, StockAllView


class TestCase(TestCase):
    def setUp(self):
        self.single_stock_url = resolve(reverse('stock:single_stock', args=['test123']))
        self.all_stock_url = resolve(reverse('stock:all_stock'))

    def test_check_match_view(self):
        self.assertEqual(self.single_stock_url.func.view_class, StockView)
        self.assertEqual(self.all_stock_url.func.view_class, StockAllView)

    def test_single_stock_not_enter_slug(self):
        with self.assertRaises(NoReverseMatch):
            url = reverse('stock:single_stock')
