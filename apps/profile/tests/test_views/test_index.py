from django.test import Client, TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):

    def test_index_response_code(self):
        # Build
        response = Client().get(reverse('profile:index'))

        # Check
        self.assertEqual(response.status_code, 200, 'Index should have a HTTP OK response')