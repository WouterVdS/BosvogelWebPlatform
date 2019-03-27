from django.test import TestCase
from django.urls import reverse


class ChangePicingTestCase(TestCase):

    def test_status_code(self):
        # Build
        response = self.client.get(reverse('rent:change_pricing'))

        # Operate
        status_code = response.status_code

        # Assert
        self.assertEqual(status_code, 200)

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('rent:change_pricing'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - Verhuur</title>' in content,
                        'The correct head title should be displayed')

    # todo when userapp is completed
    """
    def test_page_inaccessible_when_not_logged_in(self):
        # Operate
        response = self.client.get(reverse('rent:change_pricing'))

        # Assert
        self.assertEqual(response.status_code, 404)

    def test_TODO_USERS_access_restricted_to_grl_and_rental_managers(self):
        self.assertTrue(False, 'todo')

    
     test: alles op nul met db leeg, 
     niet redirect als exact gelijk
     foutmelding als exact gelijk
     correcte redirect als juist is
     prijzen gesaved als juist is
     net gesavede moet gereturned worden door get_prices()
     message displayed op redirected pagina dat het opgeslaan is
    """
