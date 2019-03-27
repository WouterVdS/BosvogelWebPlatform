from django.test import TestCase
from django.urls import reverse


class ManageRentalsTestCase(TestCase):

    def test_status_code(self):
        # Build
        response = self.client.get(reverse('rent:manage_rentals'))

        # Operate
        status_code = response.status_code

        # Assert
        self.assertEqual(status_code, 200)

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('rent:manage_rentals'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - Beheer</title>' in content,
                        'The correct head title should be displayed')

    # todo when userapp is completed
    # def test_access_restricted_to_leaders_and_rental_managers(self):
    #    self.assertTrue(False, 'todo')
