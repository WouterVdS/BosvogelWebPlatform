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
