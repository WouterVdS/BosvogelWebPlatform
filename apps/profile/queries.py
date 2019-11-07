from apps.home.models import Werkjaar
from apps.profile.models.membership import Membership


def get_active_leader_memberships(tak=None):
    result = Membership.current_year.filter(is_leader=True)
    if tak is not None:
        result = result.filter(tak=tak)
    result = result.select_related('profile')
    return result.prefetch_related()
