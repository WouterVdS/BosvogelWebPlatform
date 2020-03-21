from apps.home.models import get_workyear, Werkjaar
from apps.profile.models.membership import Membership


def get_active_leader_memberships(tak=None):
    result = Membership.current_year.filter(is_leader=True)
    if tak is not None:
        result = result.filter(tak=tak)
    result = result.select_related('profile')
    return result.prefetch_related()


def get_leader_memberships(year=None):
    if year is None:
        year = get_workyear()
    workyear = Werkjaar.objects.filter(year=year).first()
    if workyear is None:
        return Membership.objects.none()
    return Membership.objects.filter(is_leader=True, werkjaar=workyear)

