from datetime import datetime, date, time

from django.test import TestCase

from apps.agenda.models import Event, Place
from apps.home.constants import Takken, Events


class AgendaTestCase(TestCase):

    def test_str_method(self):
        # Build
        event = Event.objects.create(
            name='Testevent',
            place=Place.objects.create(name='Testplace'),
            startDate=date(2018, 3, 5),
            endDate=date(2018, 3, 6),
            startTime=time(18, 00, 0),
            endTime=time(12, 00, 0),
            description='Long description of the event',
            type=Events.JINCAFE,
            tak=Takken.JINS
        )

        # Operate
        string = str(event)

        # Check
        self.assertEqual(string,
                         'Testevent, ' + str(Place.objects.first()) +
                         ', 2018-03-05, 2018-03-06, 18:00:00, 12:00:00, Long description of the event, jncf, JIN',
                         'String method should return something readable')

    def test_event_persistence_when_deleting_place(self):
        # Build
        place = Place.objects.create()
        Event.objects.create(place=place, startDate=datetime.now())

        # Operate
        place.delete()

        # Check
        self.assertEqual(Place.objects.count(), 0, 'The place should be deleted')
        self.assertEqual(Event.objects.count(), 1, 'The event should persist if the place is deleted')
        self.assertIsNone(Event.objects.first().place, 'The location should be set to none if it gets deleted')

    def test_place_persistence_when_deleting_event(self):
        # Build
        place = Place.objects.create()
        event = Event.objects.create(place=place, startDate=datetime.now())

        # operate
        event.delete()

        # Check
        self.assertEqual(Event.objects.count(), 0, 'The event should be deleted')
        self.assertEqual(Place.objects.count(), 1, 'The place should persist when the event is deleted')

    def test_default_objects_manager_should_exist(self):
        # Build
        place = Place.objects.create()
        Event.objects.create(place=place, startDate=datetime.now())

        # Operate
        events = Event.objects.all()

        # Check
        self.assertIsNotNone(events)

    def test_rent_manager_only_returns_rental_types(self):
        # Build
        place = Place.objects.create()
        Event.objects.create(place=place, startDate=datetime.now(), type=Events.RENTAL)
        Event.objects.create(place=place, startDate=datetime.now(), type=Events.JINCAFE)
        Event.objects.create(place=place, startDate=datetime.now(), type=Events.PUBLIC_ACTIVITY)
        Event.objects.create(place=place, startDate=datetime.now(), type=Events.WORKDAY)
        Event.objects.create(place=place, startDate=datetime.now(), type=Events.RENTAL)
        Event.objects.create(place=place, startDate=datetime.now(), type=Events.LEADER_ACTIVITY)
        Event.objects.create(place=place, startDate=datetime.now(), type=Events.RENTAL)

        # Check
        for event in Event.rentals.all():
            self.assertEqual(event.type, Events.RENTAL, 'All events should of rentals should be type RENTAL')
        self.assertEqual(Event.rentals.count(), 3, 'All rental events should be returned')

    def test_default_rental_starttime_after_endtime(self):
        # Check
        self.assertTrue(Events.DEFAULT_RENT_START_TIME > Events.DEFAULT_RENT_ENDING_TIME,
                        'Scheduled rentals should be able to start and end on the same day')

    def test_save_rent_type_auto_set_times(self):
        # Build
        Event.objects.create(
            startDate=datetime.now(),
            endDate=datetime.now(),
            type=Events.RENTAL
        )

        # Operate
        rent = Event.rentals.first()

        # Check
        self.assertEqual(rent.startTime,
                         time(13, 0, 0),
                         'When saving an event, the startTime should always be 13:00')
        self.assertEqual(rent.endTime,
                         time(12, 0, 0),
                         'When saving an event, the endTime should always be 12:00')

    def test_only_set_default_times_on_rental_events(self):
        for eventType in Events.EVENT_TYPES:
            if eventType[0] is Events.RENTAL:
                continue
            # Build
            createdEvent = Event.objects.create(
                startDate=datetime.now(),
                endDate=datetime.now(),
                type=eventType[0]
            )

            # Operate
            rent = Event.objects.get(id=createdEvent.id)

            # Check
            self.assertIsNone(rent.startTime,
                              f'When saving an event of type {eventType}, no default time should be set')
            self.assertIsNone(rent.endTime,
                              f'When saving an event of type {eventType}, no default time should be set')

    def test_is_available_for_rent(self):
        # Build
        beforeDate = date(2019, 7, 10)
        startDate = date(2019, 7, 25)
        inBetweenDate = date(2019, 7, 30)
        endDate = date(2019, 8, 5)
        afterDate = date(2019, 8, 10)

        Event.objects.create(
            startDate=startDate,
            endDate=endDate,
            type=Events.RENTAL
        )

        testDates = [
            {'startDate': beforeDate, 'endDate': beforeDate, 'valid': True},
            {'startDate': beforeDate, 'endDate': startDate, 'valid': True},
            {'startDate': beforeDate, 'endDate': inBetweenDate, 'valid': False},
            {'startDate': beforeDate, 'endDate': endDate, 'valid': False},
            {'startDate': beforeDate, 'endDate': afterDate, 'valid': False},
            {'startDate': startDate, 'endDate': startDate, 'valid': False},
            {'startDate': startDate, 'endDate': inBetweenDate, 'valid': False},
            {'startDate': startDate, 'endDate': endDate, 'valid': False},
            {'startDate': startDate, 'endDate': afterDate, 'valid': False},
            {'startDate': inBetweenDate, 'endDate': inBetweenDate, 'valid': False},
            {'startDate': inBetweenDate, 'endDate': endDate, 'valid': False},
            {'startDate': inBetweenDate, 'endDate': afterDate, 'valid': False},
            {'startDate': endDate, 'endDate': endDate, 'valid': True},
            {'startDate': endDate, 'endDate': afterDate, 'valid': True},
            {'startDate': afterDate, 'endDate': afterDate, 'valid': True},
        ]

        for period in testDates:
            # Operate
            available = Event.rentals.is_available_for_rent(period['startDate'], period['endDate'])

            if period['valid']:
                # Check
                self.assertTrue(available,
                                f'{period} should be available because there is no overlap with the current one')
            else:
                # Check
                self.assertFalse(available,
                                 f'{period} should not be available for rent because it overlaps with the existing one')
