from datetime import datetime

from apps.agenda.models import Event
from apps.home.constants import Events
from apps.home.models import get_workyear


def get_vergaderingen(tak=None, all_vergaderingen=False):
    result = Event.objects.filter(type__in=[
        Events.WEEKLY_ACTIVITY,
        Events.WEEKEND,
        Events.PUBLIC_ACTIVITY])
    if all_vergaderingen:
        current_year = get_workyear()
        result = result.filter(endDate__gte=datetime(year=current_year, month=9, day=1))
    else:
        result = result.filter(endDate__gte=datetime.now())
    if tak is not None:
        result = result.filter(tak=tak)
    result = result.select_related('place')
    return result


def get_public_and_jincafe_events():
    result = Event.objects.filter(type__in=[Events.PUBLIC_ACTIVITY, Events.JINCAFE])
    result = result.filter(endDate__gte=datetime.now())
    return result
