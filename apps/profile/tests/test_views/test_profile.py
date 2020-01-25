from django.test import TestCase
from django.urls import reverse


class ProfileViewTestCase(TestCase):

    def test_profile_response_code(self):
        # Build
        # todo effectief een correct argument meegeven
        response = self.client.get(reverse('profile:profile', args=['msemkj']))

        # Check
        self.assertEqual(response.status_code, 200, 'Index should have a HTTP OK response')

    def test_using_base_html(self):
        # Build
        # todo effectief een correct argument meegeven
        response = self.client.get(reverse('profile:profile', args=['mlij']))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels' in content,
                        'The template should extend the base template')


# todo reenable
""" 
    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('profile:profile', args=['mslize']))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - NAAM VAN LEIDING </title>' in content,
                        'The correct head title should be displayed')
"""
