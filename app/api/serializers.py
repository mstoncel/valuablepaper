from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from app.api.models import Stock


class ValidationError(ValidationError):
    code = 'VALIDATION_ERROR'


class StockSerializer(serializers.Serializer):
    provider_name = serializers.CharField()
    symbol = serializers.CharField()
    real_price = serializers.FloatField()
    start_price = serializers.FloatField()

    def to_representation(self, instance):
        res = super(StockSerializer, self).to_representation(instance)
        provider_name = res.pop('provider_name')
        return {provider_name: res}


class CreateStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ('id',)
