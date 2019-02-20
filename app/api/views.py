from rest_framework.views import APIView
from app.api.serializers import StockSerializer
from app.provider.models import Provider
from rest_framework.response import Response
from rest_framework import status


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

