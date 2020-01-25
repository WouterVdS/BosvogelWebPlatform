from django.test import TestCase
from django.urls import reverse


# todo refactor test cases dat deze drie tests gestandaardiseerd kunnen worden, dus de profile:index en argumenten in variabelen steken
# todo deze eerste drie tests in alles steken, of iets van inheritance doen dat ik overerf van standaard ViewTestCases om duplicatie tegen te gaan
class IndexViewTestCase(TestCase):

    VIEW_NAME = 'profile:index'
    VIEW_ARGS = None
    TITLE_SUFFIX = 'Leiding'

    def test_index_response_code(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, self.VIEW_ARGS))

        # Check
        self.assertEqual(response.status_code, 200, f'The view {self.VIEW_NAME} should have a HTTP OK response')

    def test_using_base_html(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, self.VIEW_ARGS))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels' in content,
                        f'The template for {self.VIEW_NAME} should extend the base template')

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, self.VIEW_ARGS))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue(f'<title>De Bosvogels - {self.TITLE_SUFFIX}</title>' in content,
                        f'The correct head title should be displayed in {self.VIEW_NAME}')
