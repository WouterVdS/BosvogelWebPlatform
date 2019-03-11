from django.test import SimpleTestCase

from apps.rent.apps import RentConfig


class AppTestCase(SimpleTestCase):

    def test_app_name(self):
        # Check
        self.assertEqual(RentConfig.name, 'apps.rent', 'The app name should be correct')
