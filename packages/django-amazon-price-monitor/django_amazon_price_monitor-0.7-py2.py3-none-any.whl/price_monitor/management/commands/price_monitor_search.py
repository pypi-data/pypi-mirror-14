"""Management command for searching Amazon"""
from django.core.management.base import BaseCommand

from price_monitor.product_advertising_api.api import ProductAdvertisingAPI

from pprint import pprint


class Command(BaseCommand):

    """Command for searching ASINs and displaying their return value"""

    help = 'Searches for products at Amazon (not within the database!) with the given ASINs and prints out their details.'

    def add_arguments(self, parser):
        """
        Adds the positional argument for ASINs.

        :param parser: the argument parser
        """
        parser.add_argument('asins', nargs='+', type=str)

    def handle(self, *args, **options):
        """Searches for a product with the given ASIN."""
        asins = options['asins']
        api = ProductAdvertisingAPI()
        pprint(api.item_lookup(asins), indent=4)
