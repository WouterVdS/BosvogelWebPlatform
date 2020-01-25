from django.test import TestCase

from apps.profile.queries import get_leader_memberships


class GetLeaderMembershipsTestCase(TestCase):

    def test_return_empty_set_of_memberships_if_werkjaar_does_not_exist(self):
        # Operate
        result = get_leader_memberships(6465467)

        # Check
        self.assertIsNone(result,
                          'Should return None when requesting memberships of a werkyear that does not exist')
# todo tests uitbereiden
