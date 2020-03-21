from django.test import TestCase
from django.urls import reverse


class IndexViewTestCase(TestCase):
    VIEW_NAME = 'leiding:index'
    VIEW_ARGS = None
    TITLE_SUFFIX = 'Leiding'

    def test_index_response_code(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, args=self.VIEW_ARGS))

        # Check
        self.assertEqual(response.status_code, 200, f'The view {self.VIEW_NAME} should have a HTTP OK response')

    def test_using_base_html(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, args=self.VIEW_ARGS))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels' in content,
                        f'The template for {self.VIEW_NAME} should extend the base template')

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse(self.VIEW_NAME, args=self.VIEW_ARGS))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue(f'<title>De Bosvogels - {self.TITLE_SUFFIX}</title>' in content,
                        f'The correct head title should be displayed in {self.VIEW_NAME}')
