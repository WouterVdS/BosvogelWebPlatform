from django.test import TestCase
from django.urls import reverse


class BuildingAndTerrainTestCase(TestCase):

    def test_status_code(self):
        # Build
        response = self.client.get(reverse('rent:building_and_terrain'))

        # Operate
        status_code = response.status_code

        # Assert
        self.assertEqual(status_code, 200)

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('rent:building_and_terrain'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - Gebouw &amp; Terrein</title>' in content,
                        'The correct head title should be displayed')
