from django.test import TestCase
from django.urls import reverse


class IndexTestCase(TestCase):

    def test_title_suffix(self):
        # Operate
        response = self.client.get(reverse('agenda:index'))

        # Assert
        self.assertEqual(response.status_code, 200)
