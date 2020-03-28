from datetime import date

from django.test import TestCase

from apps.home.constants import Sex, Takken
from apps.home.models import Werkjaar
from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile
from apps.profile.models.totem import Totem


class MembershipTestCase(TestCase):

    @staticmethod
    def create_profile():
        totem = Totem.objects.create(
            totem='Ezel'
        )
        Profile.objects.create(
            first_name='Jos',
            last_name='Testermans',
            nickname='Jakke',
            email='jos@testermans.com',
            birthday=date.today(),
            sex=Sex.MALE,
            totem=totem,
            phone_number='0032477777777',
            bank_account_number='BE242424242424',
        )

    @staticmethod
    def create_werkjaar():
        Werkjaar.objects.create(year=2019)

    def create_profile_werkjaar(self):
        self.create_profile()
        self.create_werkjaar()

        profile = Profile.objects.first()
        werkjaar = Werkjaar.objects.first()

        Membership.objects.create(profile=profile,
                                  werkjaar=werkjaar)

        return profile, werkjaar

    def test_str_method(self):
        # Build
        self.create_profile()
        self.create_werkjaar()

        profile = Profile.objects.first()
        werkjaar_one = Werkjaar.objects.first()
        werkjaar_two = werkjaar_one.previous_year()
        werkjaar_three = werkjaar_two.previous_year()
        werkjaar_four = werkjaar_three.previous_year()

        membership = Membership.objects.create(
            profile=profile,
            werkjaar=werkjaar_one,
            is_leader=True,
            tak=Takken.WELPEN
        )

        membership_no_tak = Membership.objects.create(
            profile=profile,
            werkjaar=werkjaar_two,
            is_leader=True
        )

        membership_no_leader = Membership.objects.create(
            profile=profile,
            werkjaar=werkjaar_three,
            is_leader=False,
            tak=Takken.WELPEN
        )

        membership_tak_leader_name = Membership.objects.create(
            profile=profile,
            werkjaar=werkjaar_four,
            is_leader=True,
            tak=Takken.WELPEN,
            tak_leader_name='Akela'

        )

        # Check
        self.assertEqual(str(membership),
                         '2019 - 2020: Jos \'Jakke\' Testermans (leiding) - Welpen',
                         'String method should display something meaningful')

        self.assertEqual(str(membership_no_tak),
                         '2018 - 2019: Jos \'Jakke\' Testermans (leiding)',
                         'String method should display something meaningful')

        self.assertEqual(str(membership_no_leader),
                         '2017 - 2018: Jos \'Jakke\' Testermans - Welpen',
                         'String method should display something meaningful')

        self.assertEqual(str(membership_tak_leader_name),
                         '2016 - 2017: Jos \'Jakke\' Testermans als Akela (leiding) - Welpen',
                         'String method should display something meaningful')

    def test_profile_should_still_exist_if_membership_is_deleted(self):
        # Build
        self.create_profile()
        self.create_werkjaar()

        profile = Profile.objects.first()
        werkjaar = Werkjaar.objects.first()

        membership = Membership.objects.create(profile=profile,
                                               werkjaar=werkjaar)

        # Operate
        membership.delete()
        profile_count = Profile.objects.count()
        membership_count = Membership.objects.count()

        # Check
        self.assertEqual(profile_count,
                         1,
                         'Deleting a membership should not result in a deleted profile')
        self.assertEqual(membership_count,
                         0,
                         'The membership should be deleted')

    def test_membership_should_be_deleted_if_profile_is_deleted(self):
        # Build
        (profile, werkjaar) = self.create_profile_werkjaar()

        # Operate
        profile.delete()
        profile_count = Profile.objects.count()
        membership_count = Membership.objects.count()

        # Check
        self.assertEqual(membership_count,
                         0,
                         'Deleting a profile should result in a deleted membership')
        self.assertEqual(profile_count,
                         0,
                         'The profile should be deleted')

    def test_membership_should_be_deleted_if_werkjaar_is_deleted(self):
        # Build
        (profile, werkjaar) = self.create_profile_werkjaar()

        # Operate
        werkjaar.delete()
        membership_count = Membership.objects.count()
        werkjaar_count = Werkjaar.objects.count()

        # Check
        self.assertEqual(membership_count,
                         0,
                         'Deleting a werkjaar should result in a deleted membership')
        self.assertEqual(werkjaar_count,
                         0,
                         'The werkjaar should be deleted')

    def test_profile_and_werkjaar_combination_should_be_unique_in_every_membership(self):
        # Build
        self.create_profile()
        self.create_werkjaar()

        profile = Profile.objects.first()
        werkjaar = Werkjaar.objects.first()

        Membership.objects.create(profile=profile,
                                  werkjaar=werkjaar)

        # Operate
        with self.assertRaises(Exception) as raised:
            Membership.objects.create(profile=profile,
                                      werkjaar=werkjaar)

        # Check
        self.assertTrue(
            'UNIQUE constraint failed: profile_membership.profile_id, profile_membership.werkjaar_id'
            in str(raised.exception))

    def test_default_is_leader_must_be_false(self):
        # Build
        self.create_profile()
        self.create_werkjaar()

        profile = Profile.objects.first()
        werkjaar = Werkjaar.objects.first()

        membership = Membership.objects.create(profile=profile,
                                               werkjaar=werkjaar)

        # Operate
        is_leader = membership.is_leader

        # Check
        self.assertFalse(is_leader,
                         'By default, the profile must have is_leader set to false')

    def test_CurrentYearMembershipManager(self):
        # Build
        current_year = Werkjaar.objects.current_year()
        years = [
            current_year,
            current_year.previous_year(),
            current_year.next_year()
        ]
        profile = Profile.objects.create()
        for year in years:
            Membership.objects.create(
                werkjaar=year,
                profile=profile,
            )

        # Operate
        results = Membership.current_year.all()

        # Check
        for result in results:
            self.assertEqual(result.werkjaar,
                             current_year,
                             'All returned memberships must be current year')

    def test_leader_name_should_return_tak_leader_name_if_it_has_one(self):
        # Build
        profile = Profile.objects.create(first_name='Jos')
        membership = Membership.objects.create(
            werkjaar=Werkjaar.objects.current_year(),
            profile=profile,
            tak_leader_name='taknaam'
        )
        # Operate
        leader_name = membership.leader_name()

        # Check
        self.assertEqual('taknaam',
                         leader_name,
                         'When a takname is set on the membership, it should be returned by leader_name()')

    def test_leader_name_should_return_first_name_when_no_tak_leader_name(self):
        # Build
        profile = Profile.objects.create(first_name='Jos', last_name='achternaam')
        membership = Membership.objects.create(
            werkjaar=Werkjaar.objects.current_year(),
            profile=profile,
        )
        # Operate
        leader_name = membership.leader_name()

        # Check
        self.assertEqual('Jos',
                         leader_name,
                         'When no takname is set on the membership, leader_name() should only return the firstname')

    def test_leader_name_should_return_empty_string_when_no_name_set(self):
        # Build
        profile = Profile.objects.create()
        membership = Membership.objects.create(
            werkjaar=Werkjaar.objects.current_year(),
            profile=profile,
        )
        # Operate
        leader_name = membership.leader_name()

        # Check
        self.assertEqual('',
                         leader_name,
                         'When no profile name or tak leader name is set, leader_name should return an empty string')

    def test_leader_name_should_log_warning_when_returning_empty_string(self):
        with self.assertLogs(level='WARNING') as loggerWatcher:
            # Build
            profile = Profile.objects.create()
            membership = Membership.objects.create(
                werkjaar=Werkjaar.objects.current_year(),
                profile=profile,
            )
            # Operate
            leader_name = membership.leader_name()

            # Check
            self.assertIn('Function leader_name() is called on a membership and this returned an empty string.',
                          loggerWatcher.output[1],
                          'When an empty string is returned, it should log this. '
                          'This means a profile with no name is used.')
