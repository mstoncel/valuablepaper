from django.core.management import BaseCommand
from app.api.helpers import all_initial_stock


class Command(BaseCommand):
    help = 'initial all stock data'

    def handle(self, *args, **options):
        all_initial_stock()
