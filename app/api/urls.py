from django.urls import path, re_path
from app.api import views

urlpatterns = [
    path('<str:stock_symbol>', views.StockView.as_view(), name='single_stock')
]