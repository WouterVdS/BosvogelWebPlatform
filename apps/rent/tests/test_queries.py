import decimal
import logging
import random

from django.test import TestCase

from apps.rent.models import Pricing
from apps.rent.queries import get_prices


class RentQueriesTestCase(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @staticmethod
    def random_price():
        return decimal.Decimal(random.randrange(1, 100000)) / 100

    def create_pricing(self):
        return Pricing.objects.create(perPersonPerDay=self.random_price(),
                                      dailyMinimum=self.random_price(),
                                      electricitykWh=self.random_price(),
                                      waterSqM=self.random_price(),
                                      gasPerDay=self.random_price(),
                                      deposit=self.random_price(),
                                      )

    def test_get_prices_method_returning_the_latest_prices(self):
        # Build
        for x in range(0, 10):
            self.create_pricing()

        # Operate
        latest_price = get_prices()

        # Check
        self.assertEqual(latest_price,
                         Pricing.objects.order_by('-pricesSetOn').first(),
                         'get_prices() should return the latest price')

        # Extra Build
        latest_added = self.create_pricing()

        # Extra Operate
        latest_price = get_prices()

        # Extra Check
        self.assertEqual(latest_price.id,
                         latest_added.id,
                         'get_prices() should return the latest added price')

    def test_get_prices_method_returning_everything_zero_when_database_is_empty(self):
        # Operate
        pricing = get_prices()

        # Check
        self.assertIsNone(Pricing.objects.first(), 'Database should be empty for this test')
        self.assertEqual(pricing.perPersonPerDay, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.dailyMinimum, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.electricitykWh, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.waterSqM, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.gasPerDay, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.deposit, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')

    def test_get_prices_method_not_creating_pricing_when_database_empty(self):
        # Operate
        get_prices()

        # Check
        self.assertIsNone(Pricing.objects.first())
