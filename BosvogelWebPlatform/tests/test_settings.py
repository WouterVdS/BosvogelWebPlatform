from django.test import SimpleTestCase

from BosvogelWebPlatform.settings import DEFAULT_DEBUG


class SettingsTestCase(SimpleTestCase):

    def test_if_default_debug_is_false(self):
        # Check
        self.assertFalse(DEFAULT_DEBUG)
