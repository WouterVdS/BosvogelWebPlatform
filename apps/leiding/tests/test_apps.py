from django.test import SimpleTestCase

from apps.leiding.apps import LeidingConfig


class AppTestCase(SimpleTestCase):

    def test_app_name(self):
        # Check
        self.assertEqual(LeidingConfig.name, 'apps.leiding', 'The app name should be correct')
