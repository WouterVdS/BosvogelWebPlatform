from apps.home.models import get_workyear, Werkjaar
from apps.profile.models.membership import Membership
from apps.profile.models.profile import Profile


def get_active_leader_memberships(tak=None):
    result = Membership.current_year.filter(is_leader=True)
    if tak is not None:
        result = result.filter(tak=tak)
    result = result.select_related('profile')
    return result.prefetch_related()


def get_leader_profiles(year=None):
    # todo test
    if year is not None:
        year = get_workyear()
    workyear = Werkjaar.objects.get(year=year)
    return Membership.objects.filter(is_leader=True, werkjaar=workyear)

