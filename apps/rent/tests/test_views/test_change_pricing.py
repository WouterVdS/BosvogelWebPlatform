import logging

from django.core import mail
from django.test import TestCase, Client
from django.urls import reverse

from apps.rent.models import Pricing, get_prices


class ChangePricingTestCase(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_status_code(self):
        # Build
        response = self.client.get(reverse('rent:change_pricing'))

        # Operate
        status_code = response.status_code

        # Check
        self.assertEqual(status_code, 200)

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('rent:change_pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - Verhuur</title>' in content,
                        'The correct head title should be displayed')

    # todo when userapp completed
    """
    def test_page_inaccessible_when_not_logged_in(self):
        # Operate
        response = self.client.get(reverse('rent:change_pricing'))

        # Assert
        self.assertEqual(response.status_code, 404)

    def test_TODO_USERS_access_restricted_to_grl_and_rental_managers(self):
        self.assertTrue(False, 'todo')

    """

    def test_get_all_null_values_in_form_when_database_empty(self):
        # Build
        response = self.client.get(reverse('rent:change_pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertEqual(content.count('value="0"'),
                         6,
                         'All prices should be zero when no pricing in database')

    def test_get_populated_form_returned(self):
        # Build
        Pricing.objects.create(
            perPersonPerDay=22.90,
            dailyMinimum=22.90,
            electricitykWh=22.90,
            waterSqM=22.90,
            gasPerDay=22.90,
            deposit=22.90
        )
        response = self.client.get(reverse('rent:change_pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertEqual(content.count('value="22.90"'),
                         6,
                         'The latest prices should be displayed')

    def test_post_valid_form_redirect(self):
        # Build
        client = Client()

        # Operate
        response = client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '12',
            'dailyMinimum': '12',
            'electricitykWh': '12',
            'waterSqM': '12',
            'gasPerDay': '12',
            'deposit': '12',
        }, follow=True)

        # Check
        self.assertEqual(response.redirect_chain,
                         [('/verhuur/tarieven/', 302)],
                         'A successful change of price should redirect to the pricing page')

    def test_post_valid_pricing_changed(self):
        # Build
        client = Client()

        # Operate
        client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '12',
            'dailyMinimum': '12',
            'electricitykWh': '12',
            'waterSqM': '12',
            'gasPerDay': '12',
            'deposit': '12',
        })

        new_pricing = get_prices()

        # Check
        self.assertEqual(new_pricing.perPersonPerDay,
                         12,
                         'A successful change of price should change the pricing in the database')

    def test_post_valid_form_redirect_show_success_message(self):
        # Build
        client = Client()

        # Operate
        response = client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '12',
            'dailyMinimum': '12',
            'electricitykWh': '12',
            'waterSqM': '12',
            'gasPerDay': '12',
            'deposit': '12',
        }, follow=True)

        content = str(response.content)

        # Check
        self.assertTrue('Verhuurtarieven aangepast' in content,
                        'A success message should be displayed on the redirected page')

    def test_post_valid_form_redirect_show_correct_pricing(self):
        # Build
        client = Client()

        # Operate
        response = client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '12',
            'dailyMinimum': '12',
            'electricitykWh': '12',
            'waterSqM': '12',
            'gasPerDay': '12',
            'deposit': '12',
        }, follow=True)

        content = str(response.content)

        # Check
        self.assertEqual(content.count(r'\xe2\x82\xac 0'),
                         0,
                         'No price should be zero')
        self.assertTrue(r'\xe2\x82\xac 12,00' + ' per persoon, per dag' in content,
                        'Pricing per person per day should be displayed correctly')
        self.assertTrue(r'minimum van \xe2\x82\xac 12,00' + ' per dag' in content,
                        'Minimal pricing should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac 12,00' + ' per kWh' in content,
                        'Pricing for electricity should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac 12,00' + r' per m\xc2\xb3' in content,
                        'Pricing for water should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac 12,00' + ' per dag voor gas' in content,
                        'Pricing for gas should be displayed correctly')
        self.assertTrue(r'\xe2\x82\xac 12,00' + ' waarborg' in content,
                        'Pricing for deposit should be displayed correctly')

    def test_post_invalid_form_no_redirect(self):
        # Build
        client = Client()

        # Operate
        response = client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '12',
        }, follow=True)

        # Check
        self.assertEqual(response.redirect_chain,
                         [],
                         'When the form is invalid, no redirect should occur')

    def test_post_invalid_form_no_redirect_when_no_prices_changed(self):
        # Build
        Pricing.objects.create(
            perPersonPerDay=1,
            dailyMinimum=2,
            electricitykWh=3,
            waterSqM=4,
            gasPerDay=5,
            deposit=6
        )
        client = Client()

        # Operate
        response = client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '1',
            'dailyMinimum': '2',
            'electricitykWh': '3',
            'waterSqM': '4',
            'gasPerDay': '5',
            'deposit': '6',
        }, follow=True)

        # Check
        self.assertEqual(response.redirect_chain,
                         [],
                         'When no prices are changed, no redirect should occur')

    def test_post_invalid_form_error_message_on_nothing_changed(self):
        # Build
        Pricing.objects.create(
            perPersonPerDay=1,
            dailyMinimum=2,
            electricitykWh=3,
            waterSqM=4,
            gasPerDay=5,
            deposit=6
        )
        client = Client()

        # Operate
        response = client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '1',
            'dailyMinimum': '2',
            'electricitykWh': '3',
            'waterSqM': '4',
            'gasPerDay': '5',
            'deposit': '6',
        }, follow=True)

        content = str(response.content)

        # Check
        self.assertEqual(response.redirect_chain,
                         [],
                         'When no prices are changed, no redirect should occur')
        self.assertTrue('Geen verschil met de vorige tarieven' in content,
                        'When no prices are changed, the correct error message should be displayed')

    def test_email_send_when_prices_changed(self):
        # Build
        client = Client()
        Pricing.objects.create(
            perPersonPerDay=1,
            dailyMinimum=2,
            electricitykWh=3,
            waterSqM=4,
            gasPerDay=5,
            deposit=6
        )
        # Operate
        client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '12',
            'dailyMinimum': '12',
            'electricitykWh': '12',
            'waterSqM': '12',
            'gasPerDay': '12',
            'deposit': '12',
        })

        # Check
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         'Opgelet, de verhuurpijzen zijn aangepast.',
                         'An email should be send when the rent prices are changed.')

    def test_email_has_correct_data_when_prices_changed(self):
        # Build
        client = Client()
        Pricing.objects.create(
            perPersonPerDay=10,
            dailyMinimum=20,
            electricitykWh=30,
            waterSqM=40,
            gasPerDay=50,
            deposit=60
        )
        Pricing.objects.create(
            perPersonPerDay=1,
            dailyMinimum=2,
            electricitykWh=3,
            waterSqM=4,
            gasPerDay=5,
            deposit=6
        )
        # Operate
        client.post(reverse('rent:change_pricing'), {
            'perPersonPerDay': '12',
            'dailyMinimum': '12',
            'electricitykWh': '12',
            'waterSqM': '12',
            'gasPerDay': '12',
            'deposit': '12',
        })
        mail_body = mail.outbox[0].body

        # Check
        self.assertTrue('€ 1.00 --> € 12.00' in mail_body,
                        'The email should reflect the correct changes to the pricing')
        self.assertTrue('€ 2.00 --> € 12.00' in mail_body,
                        'The email should reflect the correct changes to the pricing')
        self.assertTrue('€ 3.00 --> € 12.00' in mail_body,
                        'The email should reflect the correct changes to the pricing')
        self.assertTrue('€ 4.00 --> € 12.00' in mail_body,
                        'The email should reflect the correct changes to the pricing')
        self.assertTrue('€ 5.00 --> € 12.00' in mail_body,
                        'The email should reflect the correct changes to the pricing')
        self.assertTrue('€ 6.00 --> € 12.00' in mail_body,
                        'The email should reflect the correct changes to the pricing')
