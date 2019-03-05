from django.test import SimpleTestCase

from apps.place.apps import PlaceConfig


class AppTestCase(SimpleTestCase):

    def test_app_name(self):
        # Check
        self.assertEqual(PlaceConfig.name, 'apps.place', 'The app name should be correct')
