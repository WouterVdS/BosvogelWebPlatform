from django.test import SimpleTestCase

from apps.profile.apps import ProfileConfig


class AppTestCase(SimpleTestCase):

    def test_app_name(self):
        # Check
        self.assertEqual(ProfileConfig.name, 'apps.profile', 'The app name should be correct')
