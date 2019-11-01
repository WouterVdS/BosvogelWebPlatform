from django.test import TestCase, override_settings
from django.urls import reverse


class IndexTestCase(TestCase):

    def test_title_suffix(self):
        # Operate
        response = self.client.get(reverse('home:index'))

        # Assert
        self.assertEqual(response.status_code, 200)

    @override_settings(DEBUG=True)
    def test_when_debug_mode_is_on_it_should_be_graphically_displayed(self):
        # Build

        # Operate
        response = self.client.get(reverse('home:index'))
        content = str(response.content)

        # Check
        self.assertTrue('debug' in content,
                        'It should display something to the user that Debug mode is active')

    @override_settings(DEBUG=False)
    def test_when_debug_mode_is_off_nothing_special_should_be_displayed(self):
        # Build

        # Operate
        response = self.client.get(reverse('home:index'))
        content = str(response.content)

        # Check
        self.assertTrue('debug' not in content,
                        'No mention of debug mode should be shown to the user')
