from django.test import SimpleTestCase

from apps.takken.apps import TakkenConfig


class AppTestCase(SimpleTestCase):

    def test_app_name(self):
        # Check
        self.assertEqual(TakkenConfig.name, 'apps.takken', 'The app name should be correct')
