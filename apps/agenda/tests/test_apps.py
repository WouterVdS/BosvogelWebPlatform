from django.test import SimpleTestCase

from apps.agenda.apps import AgendaConfig


class AppTestCase(SimpleTestCase):

    def test_app_name(self):
        # Check
        self.assertEqual(AgendaConfig.name, 'apps.agenda', 'The app name should be correct')
