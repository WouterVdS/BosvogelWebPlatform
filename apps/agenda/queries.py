from datetime import datetime

from apps.agenda.models import Event
from apps.home.constants import Events


def get_vergaderingen(tak=None):
    result = Event.objects.filter(type__in=[
        Events.WEEKLY_ACTIVITY,
        Events.WEEKEND,
        Events.PUBLIC_ACTIVITY])

    result = result.filter(endDate__gte=datetime.now())
    if tak is not None:
        result = result.filter(tak=tak)
    result = result.prefetch_related('place')
    return result


def get_public_and_jincafe_events():
    result = Event.objects.filter(type__in=[Events.PUBLIC_ACTIVITY, Events.JINCAFE])
    result = result.filter(endDate__gte=datetime.now())
    return result
