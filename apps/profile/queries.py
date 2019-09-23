from apps.home.models import Werkjaar
from apps.profile.models.membership import Membership


def get_active_leader_memberships(tak=None):
    current_year = Werkjaar.objects.current_year()
    result = Membership.objects.filter(werkjaar=current_year, is_leader=True)
    if tak is not None:
        result = result.filter(tak=tak)
    return result.prefetch_related()
