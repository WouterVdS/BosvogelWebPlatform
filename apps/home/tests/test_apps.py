from django.test import SimpleTestCase

from apps.home.apps import HomeConfig


class AppTestCase(SimpleTestCase):

    def test_app_name(self):
        # Check
        self.assertEqual(HomeConfig.name, 'apps.home', 'The app name should be correct')
