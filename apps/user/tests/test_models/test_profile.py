from datetime import date

from django.test import TestCase

from apps.user.models import MALE
from apps.user.models import Profile


class ProfileTestCase(TestCase):
    profile = None

    def setUp(self):
        self.profile = Profile.objects.create(
            first_name='Jos',
            last_name='Testermans',
            nickname='Jakke',
            email='jos@testermans.com',
            birthday=date.today(),
            sex=MALE,
            phoneNr='0032477777777',
            bank_account_number='BE242424242424',
            active=True,
        )

    def test_str_method(self):
        # Check
        self.assertEqual(str(self.profile),
                         'Jos \'Jakke\' Testermans',
                         'String method should display something meaningful')

    def test_str_method_no_nickname(self):
        # Operate
        self.profile.nickname = None

        # Check
        self.assertEqual(str(self.profile),
                         'Jos Testermans',
                         'String method should display something meaningful')
