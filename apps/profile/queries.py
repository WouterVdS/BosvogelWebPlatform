from apps.home.models import Werkjaar
from apps.profile.models.profile import Profile


def get_active_leaders(tak=None):  # todo test thoroughly and optimize
    current_year = Werkjaar.objects.current_year()
    result = Profile.objects.filter(membership__is_leader=True, membership__werkjaar=current_year)
    if tak is not None:
        result = result.filter(membership__tak=tak)
    return result
