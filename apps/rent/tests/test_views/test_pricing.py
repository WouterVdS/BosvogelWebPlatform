import logging

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from apps.rent.models import Pricing


class PricingTestCase(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_status_code(self):
        # Build
        response = self.client.get(reverse('rent:pricing'))

        # Operate
        status_code = response.status_code

        # Assert
        self.assertEqual(status_code, 200)

    def test_using_base_html(self):
        # Build
        response = self.client.get(reverse('rent:pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels' in content,
                        'The view template should extend the base template')

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('rent:pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - Tarieven</title>' in content,
                        'The correct head title should be displayed')

    def test_pricing_displayed(self):
        # Build
        response = self.client.get(reverse('rent:pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('per persoon, per dag' in content,
                        'Pricing per person per day should be displayed')
        self.assertTrue('minimum' in content,
                        'Minimal pricing should be displayed')
        self.assertTrue('per kWh' in content,
                        'Pricing for electricity should be displayed')
        self.assertTrue(r'per m\xc2\xb3' in content,
                        'Pricing pfor water should be displayed')
        self.assertTrue('per dag voor gas' in content,
                        'Pricing for gas should be displayed')
        self.assertTrue('waarborg' in content,
                        'Pricing for deposit should be displayed')

    def test_pricing_zero_with_empty_database(self):
        # Build
        response = self.client.get(reverse('rent:pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertEqual(content.count(r'\xe2\x82\xac 0'),
                         6,
                         'All prices should be zero when the database is empty')

    def test_pricing_correctly_displayed(self):
        # Build
        pricing = Pricing.objects.create(
            perPersonPerDay=1,
            dailyMinimum=2,
            electricitykWh=3,
            waterSqM=4,
            gasPerDay=5,
            deposit=6
        )
        response = self.client.get(reverse('rent:pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertEqual(content.count(r'\xe2\x82\xac 0'),
                         0,
                         'No price should be zero')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.perPersonPerDay) + ',00' + ' per persoon, per dag' in content,
                        'Pricing per person per day should be displayed correctly')
        self.assertTrue(r'minimum van \xe2\x82\xac ' + str(pricing.dailyMinimum) + ',00' + ' per dag' in content,
                        'Minimal pricing should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.electricitykWh) + ',00' + ' per kWh' in content,
                        'Pricing for electricity should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.waterSqM) + ',00' + r' per m\xc2\xb3' in content,
                        'Pricing for water should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.gasPerDay) + ',00' + ' per dag voor gas' in content,
                        'Pricing for gas should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.deposit) + ',00' + ' waarborg' in content,
                        'Pricing for deposit should be displayed correctly')

    def test_latest_pricing_displayed(self):
        # Build
        Pricing.objects.create(
            perPersonPerDay=6,
            dailyMinimum=5,
            electricitykWh=4,
            waterSqM=3,
            gasPerDay=2,
            deposit=1
        )

        pricing = Pricing.objects.create(
            perPersonPerDay=1,
            dailyMinimum=2,
            electricitykWh=3,
            waterSqM=4,
            gasPerDay=5,
            deposit=6
        )
        response = self.client.get(reverse('rent:pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertEqual(content.count(r'\xe2\x82\xac 0'),
                         0,
                         'No price should be zero')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.perPersonPerDay) + ',00' + ' per persoon, per dag' in content,
                        'Pricing per person per day should be displayed correctly')
        self.assertTrue(r'minimum van \xe2\x82\xac ' + str(pricing.dailyMinimum) + ',00' + ' per dag' in content,
                        'Minimal pricing should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.electricitykWh) + ',00' + ' per kWh' in content,
                        'Pricing for electricity should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.waterSqM) + ',00' + r' per m\xc2\xb3' in content,
                        'Pricing for water should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.gasPerDay) + ',00' + ' per dag voor gas' in content,
                        'Pricing for gas should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac ' + str(pricing.deposit) + ',00' + ' waarborg' in content,
                        'Pricing for deposit should be displayed correctly')

    def test_email_send_when_view_called_and_pricing_empty(self):
        # Operate
        self.client.get(reverse('rent:pricing'))

        # Check
        self.assertEqual(len(mail.outbox),
                         1,
                         'An email should be send when pricing is empty and the pricing page is called')
        self.assertEqual(mail.outbox[0].subject,
                         'ERROR - Verhuur prijzen zijn nog niet gezet!',
                         'The email send when no prices are set should contain the correct message')
