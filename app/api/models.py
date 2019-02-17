from django.db import models

from app.provider.models import Provider


class Stock(models.Model):
    symbol = models.CharField(max_length=15)
    real_price = models.FloatField()
    start_price = models.FloatField()
    title = models.CharField(max_length=150, null=True)
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT,
                                 related_name='provider')

    class Meta:
        db_table = 'stock'
