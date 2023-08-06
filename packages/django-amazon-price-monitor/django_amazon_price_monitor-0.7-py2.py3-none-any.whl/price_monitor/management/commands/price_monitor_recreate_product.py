"""Management command for recreating a product"""
from django.core.management.base import BaseCommand

from price_monitor.models import Product


class Command(BaseCommand):
    help = 'Recreates a product with the given asin. If product already exists, it is deleted.'

    def add_arguments(self, parser):
        """
        Adds the positional argument for ASIN

        :param parser: the argument parser
        """
        parser.add_argument('asin', nargs=1, type=str)

    def handle(self, *args, **options):
        """Recreates the product with given ASIN"""
        asin = options['asin'][0]
        product, created = Product.objects.get_or_create(asin=asin)
        if not created:
            product.delete()
            Product.objects.create(asin=asin)
