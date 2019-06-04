from django.test import SimpleTestCase

from apps.user.apps import UserConfig


class AppTestCase(SimpleTestCase):

    def test_app_name(self):
        # Check
        self.assertEqual(UserConfig.name, 'apps.user', 'The app name should be correct')
