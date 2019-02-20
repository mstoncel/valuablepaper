from app.provider.models import Provider
from app.api.models import Stock


def all_initial_stock():
    providers = Provider.objects.all()
    for provider in providers:
        if provider.status.lower() == 'active':
            adapter = provider.get_adapter(provider=provider)
            response = adapter.initial_all_stock_data()
            Stock.objects.bulk_create(response)
