from datetime import datetime

from django.test import TestCase

from apps.agenda.queries import get_vergaderingen
from apps.agenda.tests.test_queries.helpers import create_test_data
from apps.home.constants import Events, Takken


class GetVergaderingenTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def test_it_should_only_return_event_type_of_weekly_activity_or_weekend(self):
        # Operate
        events = get_vergaderingen()

        # Check
        self.assertIsNotNone(events)
        for event in events:
            self.assertTrue((event.type == Events.WEEKLY_ACTIVITY) or (event.type == Events.WEEKEND),
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
            if event.startTime:
                new_date = new_date.replace(hour=event.startTime.hour,
                                            minute=event.startTime.minute,
                                            second=event.startTime.second)
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
