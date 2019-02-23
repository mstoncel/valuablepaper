from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from app.api.models import Stock
from app.api.serializers import StockSerializer, StockAllSerializer
from app.provider.models import Provider
from rest_framework.response import Response
from rest_framework import status
import django_filters.rest_framework
from rest_framework.pagination import PageNumberPagination


class StockFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="real_price",
                                            lookup_expr='gte')
    provider = django_filters.CharFilter(field_name='provider__name',
                                         lookup_expr='iexact')

    class Meta:
        model = Stock
        fields = ['symbol', 'provider', 'min_price']


class StockAllView(ListAPIView):
    serializer_class = StockAllSerializer
    queryset = Stock.objects.all()
    filter_class = StockFilter
    pagination_class = PageNumberPagination


class StockView(APIView):
    def get(self, *args, **kwargs: dict) -> dict:
        search = self.request.GET.get('name')
        stock_symbol = kwargs.get('stock_symbol')
        providers = Provider.objects.filter()
        if search:
            providers.filter()
        response_data = []
        for provider in providers:
            # check all provider
            if search:
                if provider.name != search.lower():
                    continue
            adapter = provider.get_adapter(provider=provider)
            if not provider.status.lower() == 'active':
                continue
            response = adapter.initial_stock_data(stock_symbol)
            if response:
                response_data.append(response)
                response.update(dict(
                    provider=provider.pk
                ))
        serializer = StockSerializer(data=response_data, many=True)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
