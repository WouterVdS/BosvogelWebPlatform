from datetime import date

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from apps.home.constants import Sex
from apps.profile.models.profile import Profile
from apps.profile.models.totem import Totem


# noinspection PyUnusedLocal
class ProfileTestCase(TestCase):
    @staticmethod
    def generate_profile():
        totem = Totem.objects.create(
            totem='Ezel'
        )
        return Profile(
            first_name='Jos',
            last_name='Testermans',
            nickname='Jakke',
            email='jos@testermans.com',
            public_email='jos@bosvogels.be',
            birthday=date.today(),
            sex=Sex.MALE,
            totem=totem,
            phone_number='0032477777777',
            bank_account_number='BE242424242424',
        )

    def test_str_method(self):
        # Check
        self.assertEqual(str(self.generate_profile()),
                         'Jos \'Jakke\' Testermans',
                         'String method should display something meaningful')

    def test_str_method_no_nickname(self):
        # Operate
        profile = self.generate_profile()
        profile.nickname = None

        # Check
        self.assertEqual(str(profile),
                         'Jos Testermans',
                         'String method should display something meaningful')

    def test_email_should_be_unique(self):
        # Build
        self.generate_profile().save()
        profile_two = Profile(
            email=self.generate_profile().email
        )

        # Check
        with self.assertRaises(IntegrityError):
            profile_two.save()

    def test_public_email_should_be_unique(self):
        # Build
        self.generate_profile().save()
        profile_two = Profile(
            public_email=self.generate_profile().public_email
        )

        # Check
        with self.assertRaises(IntegrityError):
            profile_two.save()

    def test_totem_should_be_deleted_when_profile_is_deleted(self):
        # Build
        self.generate_profile().save()

        # Operate
        Profile.objects.first().delete()
        totem_count = Totem.objects.all().count()

        # Check
        self.assertEqual(0,
                         totem_count,
                         'Totem should be deleted when the profile is deleted')

    def test_profile_should_remain_when_totem_is_deleted(self):
        # Build
        self.generate_profile().save()

        # Operate
        Totem.objects.first().delete()
        profile_count = Profile.objects.count()

        # Check
        self.assertEqual(1,
                         profile_count,
                         'When the totem is deleted, the profile should remain')

    def test_validation_of_international_phoneNr(self):
        # Build
        profile = self.generate_profile()

        profile.phone_number = '0477556655'

        # Operate
        with self.assertRaises(ValidationError) as raised:
            profile.full_clean()

        # Check
        self.assertTrue('beginnen met 0032' in str(raised.exception),
                        'But it is: ' + str(raised.exception))

    def test_validation_of_bankAccountNumber(self):
        # Build
        profile = self.generate_profile()
        profile.bank_account_number = 'BE2144547wrong'

        # Operate
        with self.assertRaises(ValidationError) as context:
            profile.full_clean()

        # Check
        self.assertTrue('Rekeningnummer moet in het volgende formaat' in str(context.exception),
                        'But it is: ' + str(context.exception))
