from django.test import TestCase, Client
from django.urls import reverse

from apps.home.constants import Takken


class TakviewGeneralTestCase(TestCase):

    def test_index_response_code(self):
        # Operate
        response = Client().get(reverse('takken:index'))

        # Check
        self.assertEqual(response.status_code, 200, 'Index should have a HTTP OK response')

    def test_tak_views_for_all_takken_response_code(self):
        for (abbreviation, tak) in Takken.TAKKEN:
            # Operate
            response = Client().get(reverse('takken:tak', args=[tak.lower()]))
            content = str(response.content)

            # Check
            self.assertEqual(response.status_code, 200,
                             'Takview for ' + tak.lower() + ' should have a HTTP OK response')
            self.assertTrue('<title>De Bosvogels -  ' + tak + '</title>' in content,
                            'The right page should be displayed for ' + tak)

    def test_redirect_on_wrong_takname_in_url(self):
        # Operate
        response = Client().get(reverse('takken:tak', args=['gibberish']))

        # Check
        self.assertEqual(response.status_code, 302,
                         'When going to a faulty tak link, it should be redirected')
        self.assertEqual(response.url, '/takken/',
                         'The page redirected to should be the takken index')

    def test_after_leader_view_response_code(self):
        # Operate
        response = Client().get(reverse('takken:afterleader'))

        # Check
        self.assertEqual(response.status_code, 200, 'Afterleader view should have a HTTP OK response')
