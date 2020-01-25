from datetime import date

from django.test import TestCase
from django.urls import reverse


# todo tests uitbereiden
class IndexYearViewTestCase(TestCase):

    def test_index_year_response_code(self):
        # Build
        response = self.client.get(reverse('profile:index_year', args=[date.today().year]))

        # Check
        self.assertEqual(response.status_code, 200, 'Index should have a HTTP OK response')

    def test_using_base_html(self):
        # Build
        response = self.client.get(reverse('profile:index_year', args=[date.today().year]))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels' in content,
                        'The view template should extend the base template')

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('profile:index_year', args=[date.today().year]))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - Leiding</title>' in content,
                        'The correct head title should be displayed')
