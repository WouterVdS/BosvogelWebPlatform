from datetime import datetime, date, time, timedelta

from apps.agenda.models import Event
from apps.home.constants import Events, Takken


def create_test_data():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day

    # Create all types
    for eventType in Events.EVENT_TYPES:
        Event.objects.create(
            name='test event',
            type=eventType[0],
            startDate=now,
            tak=Takken.KAPOENEN
        )

    # Create for all takken
    for tak in Takken.TAKKEN:
        Event.objects.create(
            name='test event',
            type=Events.WEEKLY_ACTIVITY,
            tak=tak[0],
            startDate=now
        )

        # Create weekly activities with mixed days
        for x in range(10):
            Event.objects.create(
                name='test event',
                type=Events.WEEKLY_ACTIVITY,
                startDate=date(year, month, 1 + x),
                startTime=time(12, 0, 0),
                tak=tak[0],
            )
            Event.objects.create(
                name='test event',
                type=Events.WEEKLY_ACTIVITY,
                startDate=date(year, month, 11 - x),
                startTime=time(11, 0, 0),
                tak=tak[0],
            )

        # Create events that are passed, but in current workyear
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year, month, day) - timedelta(days=1),
            name='past event from current workyear',
            tak=tak[0],
        )

        # Create events in the past workyears
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year - 1, month, day),
            name='past event',
            tak=tak[0],
        )
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year - 2, month, day),
            endDate=date(year - 1, month, day),
            name='past event',
            tak=tak[0],
        )
