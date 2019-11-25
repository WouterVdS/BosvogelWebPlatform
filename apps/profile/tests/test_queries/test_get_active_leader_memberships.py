from django.test import TestCase

from apps.home.constants import Takken
from apps.home.models import Werkjaar
from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile
from apps.profile.queries import get_active_leader_memberships


class GetActiveLeaderMembershipsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        current_year = Werkjaar.objects.current_year()
        last_year = current_year.previous_year()

        # Create members and leaders for each tak for the current year and last year

        for tak in Takken.TAKKEN:
            for year in [current_year, last_year]:
                # Member
                Membership.objects.create(
                    werkjaar=year,
                    is_leader=False,
                    tak=tak[0],
                    profile=Profile.objects.create(
                        first_name='Jos'
                    )
                )

                # Leader
                Membership.objects.create(
                    werkjaar=year,
                    is_leader=True,
                    tak=tak[0],
                    tak_leader_name='Akela',
                    profile=Profile.objects.create(
                        first_name='Jef'
                    )
                )

    def test_it_should_return_only_leaders(self):
        # Operate
        memberships = get_active_leader_memberships()

        # Assert
        for membership in memberships:
            self.assertTrue(membership.is_leader,
                            'Only leaders should be returned')

    def test_it_should_return_profiles_with_an_active_membership_this_year(self):
        # Operate
        memberships = get_active_leader_memberships()

        # Assert
        for membership in memberships:
            self.assertEqual(membership.werkjaar, Werkjaar.objects.current_year(),
                             'Only memberships of this workyear should be returned')

    def test_it_should_return_leaders_of_all_takken(self):
        # Operate
        memberships = get_active_leader_memberships()
        returned_takken = memberships.values_list('tak', flat=True)

        # Assert
        for tak in Takken.TAKKEN:
            self.assertIn(tak[0], returned_takken,
                          'Leaders from all takken should be returned')

    def test_it_should_only_return_leaders_of_the_selected_tak(self):
        for tak in Takken.TAKKEN:
            # Operate
            memberships = get_active_leader_memberships(tak=tak[0])

            self.assertTrue(len(memberships) > 0)
            for membership in memberships:
                self.assertEqual(tak[0], membership.tak,
                                 'The tak should be correct')
                self.assertTrue(membership.is_leader,
                                'Only leaders should be returned')
                self.assertEqual(Werkjaar.objects.current_year(), membership.werkjaar,
                                 'It should only return memberships from the current year')
