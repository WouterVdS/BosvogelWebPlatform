from datetime import datetime, date, time

from django.test import TestCase

from apps.agenda.models import Event, Place, dangling_rental_event_count
from apps.home.constants import Takken, Events
from apps.rent.models import Reservation


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
                         ', 2018-03-05, 2018-03-06, 18:00:00, 12:00:00, Long description of the event, Jincafé, Jins',
                         'String method should return something readable')

    def test_save_should_fill_in_endDate_when_not_defined(self):
        # Build
        Event.objects.create(
            startDate=datetime.now(),
            type=Events.WEEKLY_ACTIVITY
        )

        # Operate
        event = Event.objects.first()

        # Check
        self.assertEqual(event.endDate,
                         event.startDate,
                         'When endDate is not provided, startDate should be used as endDate. '
                         f'In this case: startDate = {event.startDate}, endDate = {event.endDate}')

    def test_save_should_not_overwrite_endDate_when_provide(self):
        # Build
        now = datetime.now()
        initial_end_date = date(now.year - 1, now.month, now.day)
        Event.objects.create(
            startDate=datetime.now(),
            endDate=initial_end_date,
            type=Events.WEEKLY_ACTIVITY
        )
        # Operate
        event = Event.objects.first()

        # Check
        self.assertEqual(event.endDate,
                         initial_end_date,
                         f'The set endDate ({initial_end_date}) should equal the saved endDate ({event.endDate})')

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

        for event_type in Events.EVENT_TYPES:
            Event.objects.create(place=place, startDate=datetime.now(), type=event_type[0])

        for x in range(3):
            Event.objects.create(place=place, startDate=datetime.now(), type=Events.RENTAL)

        # Check
        for event in Event.rentals.all():
            self.assertEqual(event.type, Events.RENTAL, 'All events should of rentals should be type RENTAL')
        self.assertEqual(Event.rentals.count(), 4, 'All rental events should be returned')

    def test_ordering_on_startdate_first(self):
        # Build
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(2019, 8, 5)
        )
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(2019, 8, 4)
        )
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(2019, 8, 6)
        )

        # Operate
        events = Event.objects.all()

        # Check
        prev_date = date.min
        for event in events:
            self.assertTrue(prev_date < event.startDate,
                            f'The current date ({event.startDate}) should come after the next date ({prev_date})')
            prev_date = event.startDate

    def test_ordering_on_startTime_after_startDate(self):
        # Build
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(2019, 8, 5),
            startTime=time(12, 0, 0)
        )
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(2019, 8, 5),
            startTime=time(11, 0, 0)
        )
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(2019, 8, 5),
            startTime=time(13, 0, 0)
        )

        # Operate
        events = Event.objects.all()

        # Check
        prev_time = time.min
        for event in events:
            self.assertTrue(prev_time < event.startTime,
                            f'The current time ({event.startTime}) should come after the next time ({prev_time})')
            prev_time = event.startTime

    def test_default_rental_starttime_after_endtime(self):
        # Check
        self.assertTrue(Events.DEFAULT_RENT_START_TIME > Events.DEFAULT_RENT_ENDING_TIME,
                        'Scheduled rentals should be able to start and end on the same day')

    def test_new_rental_(self):
        # Build
        start = date(2019, 7, 1)
        end = date(2019, 1, 10)
        name = 'Verhuur - Testevent'
        Event.rentals.new_rental(start, end, name)

        # Operate
        rent = Event.rentals.first()
        eventCount = Event.objects.count()

        # Check
        self.assertEqual(rent.startDate,
                         start,
                         'The startdate should be set correctly')
        self.assertEqual(rent.endDate,
                         end,
                         'The enddate should be set correctly')
        self.assertEqual(rent.name,
                         name,
                         'The name should be set correctly')
        self.assertEqual(eventCount,
                         1,
                         'Only one event should be created')

    def test_new_rental_automatically_set_times(self):
        # Build
        Event.rentals.new_rental(datetime.now(), datetime.now(), 'Verhuur - Testevent')

        # Operate
        rent = Event.rentals.first()

        # Check
        self.assertEqual(rent.startTime,
                         time(13, 0, 0),
                         'When saving an event, the startTime should always be 13:00')
        self.assertEqual(rent.endTime,
                         time(12, 0, 0),
                         'When saving an event, the endTime should always be 12:00')

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

    def test_dangling_rental_event_count_zero(self):
        # Build
        for event_type in Events.EVENT_TYPES:
            if event_type[0] == Events.RENTAL:
                break
            Event.objects.create(
                type=event_type[0],
                startDate=date.today(),
            )

        # Operate
        result = dangling_rental_event_count()

        # Check
        self.assertEqual(result,
                         0,
                         'No dangling rental events should be found')

    def test_dangling_rental_event_count(self):
        # Build
        for event_type in Events.EVENT_TYPES:
            Event.objects.create(
                type=event_type[0],
                startDate=date.today(),
            )
        rental_event = Event.objects.create(
            type=Events.RENTAL,
            startDate=date.today(),
        )
        Reservation.objects.create(
            period=rental_event,
            numberOfPeople=20
        )

        # Operate
        result = dangling_rental_event_count()

        # Check
        self.assertEqual(result,
                         1,
                         'Only one dangling event should be returned, the one created without reservation')
