from datetime import datetime, date

from django.test import TestCase

from apps.agenda.queries import get_vergaderingen
from apps.agenda.tests.test_queries.helpers import create_test_data
from apps.home.constants import Events, Takken
from apps.home.models import Werkjaar


class GetVergaderingenTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def test_it_should_only_return_event_type_of_weekly_activity_or_weekend_or_public_events(self):
        # Operate
        events = get_vergaderingen()

        # Check
        self.assertIsNotNone(events)
        for event in events:
            self.assertTrue((event.type == Events.WEEKLY_ACTIVITY)
                            or (event.type == Events.WEEKEND)
                            or event.type == Events.PUBLIC_ACTIVITY,
                            f'It should only return weekly activities and weekends, '
                            f'type of this event: {event.get_type_display()}')

    def test_it_should_sort_the_events(self):
        # Operate
        events = get_vergaderingen()

        # Check
        previous_date = datetime.min
        self.assertIsNotNone(events)
        for event in events:
            new_date = datetime(event.startDate.year, event.startDate.month, event.startDate.day)
            self.assertTrue(previous_date <= new_date, 'Earlier events should be first')
            previous_date = new_date

    def test_it_should_return_the_correct_tak_only(self):
        # Operate
        events = get_vergaderingen(Takken.KAPOENEN)

        # Check
        self.assertIsNotNone(events)
        for event in events:
            self.assertEqual(event.tak, Takken.KAPOENEN,
                             'It should only return the correct tak')

    def test_it_should_not_return_passed_events(self):
        # Operate
        events = get_vergaderingen()

        # Check
        self.assertIsNotNone(events)
        for event in events:
            self.assertFalse('past event' in event.name,
                             f'It should not include events from the past:'
                             f'startDate = {event.startDate}'
                             f', endDate = {event.endDate}')

    def test_it_should_return_passed_events_when_all_vergaderingen_is_True(self):
        # Operate
        events = get_vergaderingen(Takken.KAPOENEN, True)

        current_workyear = Werkjaar.objects.current_year()

        # Check
        self.assertIsNotNone(events)
        has_passed_events = False
        has_future_events = False
        has_events_from_last_year = False
        for event in events:
            if Werkjaar.objects.current_year(event.startDate).year == current_workyear.year:
                if event.startDate >= date.today():
                    has_future_events = True
                if event.endDate < date.today():
                    has_passed_events = True
            if get_workyear(event.endDate) < current_workyear:  # pragma:no cover
                has_events_from_last_year = True

        self.assertTrue(has_future_events,
                        'When parameter all_vergaderingen is True, it should also return future events')
        self.assertTrue(has_passed_events,
                        'When parameter all_vergaderingen is True, it should return events that are before today')
        self.assertFalse(has_events_from_last_year,
                         'Events from a previous workyear should never be returned')
