from django.test import TestCase
from django.urls import reverse


class PhotosTestCase(TestCase):

    def test_status_code(self):
        # Build
        response = self.client.get(reverse('rent:photos'))

        # Operate
        status_code = response.status_code

        # Assert
        self.assertEqual(status_code, 200)

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('rent:photos'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - Verhuur Foto&#39;s</title>' in content,
                        'The correct head title should be displayed')
