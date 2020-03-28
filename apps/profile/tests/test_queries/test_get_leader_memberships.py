from django.test import TestCase

from apps.home.constants import Takken
from apps.home.models import Werkjaar
from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile
from apps.profile.queries import get_leader_memberships


class GetLeaderMembershipsTestCase(TestCase):

    def test_return_None_if_werkjaar_does_not_exist(self):
        # Operate
        result = get_leader_memberships(6465467)

        # Check
        self.assertEqual(result.count(),
                         0,
                         'Should return empty queryset when requesting memberships of a werkyear that does not exist')

    def test_return_None_if_no_memberships_exist(self):
        # Build
        current_year = Werkjaar.objects.current_year()
        last_year = current_year.previous_year()

        Membership.objects.create(
            werkjaar=current_year,
            is_leader=False,
            tak=Takken.TAKKEN[0][0],
            profile=Profile.objects.create(
                first_name='Jos'
            )
        )
        Membership.objects.create(
            werkjaar=last_year,
            is_leader=True,
            tak=Takken.TAKKEN[0][0],
            profile=Profile.objects.create(
                first_name='Jos'
            )
        )

        # Operate
        result = get_leader_memberships()
        # Check
        self.assertEqual(result.count(),
                         0,
                         'Should return empty queryset when no memberships for leaders exist in the given year')

    def test_return_correct_memberships_when_no_year_given(self):
        # Build
        current_year = Werkjaar.objects.current_year()
        last_year = current_year.previous_year()

        Membership.objects.create(
            werkjaar=current_year,
            is_leader=True,
            tak=Takken.TAKKEN[0][0],
            profile=Profile.objects.create(
                first_name='Jos'
            )
        )
        Membership.objects.create(
            werkjaar=last_year,
            is_leader=True,
            tak=Takken.TAKKEN[0][0],
            profile=Profile.objects.create(
                first_name='Patrick'
            )
        )

        # Operate
        result = get_leader_memberships()

        # Check
        self.assertEqual(result.count(),
                         1,
                         'Only one membership should be in the result')
        self.assertEqual(result.first().profile.first_name, 'Jos',
                         'The membership of this year should be returned')

    def test_return_correct_memberships_when_a_year_is_given(self):
        # Build
        current_year = Werkjaar.objects.current_year()
        last_year = current_year.previous_year()

        Membership.objects.create(
            werkjaar=current_year,
            is_leader=True,
            tak=Takken.TAKKEN[0][0],
            profile=Profile.objects.create(
                first_name='Jos'
            )
        )
        Membership.objects.create(
            werkjaar=last_year,
            is_leader=True,
            tak=Takken.TAKKEN[0][0],
            profile=Profile.objects.create(
                first_name='Patrick'
            )
        )

        # Operate
        result = get_leader_memberships(last_year.year)

        # Check
        self.assertEqual(result.count(),
                         1,
                         'Only one membership should be in the result')
        self.assertEqual(result.first().profile.first_name, 'Patrick',
                         'The membership of last year should be returned')

    def test_return_only_leader_memberships(self):
        # Build
        current_year = Werkjaar.objects.current_year()

        Membership.objects.create(
            werkjaar=current_year,
            is_leader=True,
            tak=Takken.TAKKEN[0][0],
            profile=Profile.objects.create(
                first_name='Jos'
            )
        )
        Membership.objects.create(
            werkjaar=current_year,
            is_leader=False,
            tak=Takken.TAKKEN[0][0],
            profile=Profile.objects.create(
                first_name='Patrick'
            )
        )

        # Operate
        result = get_leader_memberships()

        # Check
        self.assertEqual(result.count(),
                         1,
                         'Only one membership should be in the result')
        self.assertEqual(result.first().profile.first_name,
                         'Jos',
                         'Only the leader membership should be returned')
