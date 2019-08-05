from django.test import TestCase

from apps.agenda.queries import get_public_and_jincafe_events
from apps.agenda.tests.test_queries.helpers import create_test_data
from apps.home.constants import Events


class GetPublicAndJincafeEventsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def test_it_should_only_return_event_type_of_public_activity_or_jincafe(self):
        # Operate
        events = get_public_and_jincafe_events()

        # Check
        self.assertIsNotNone(events)
        for event in events:
            self.assertTrue((event.type == Events.PUBLIC_ACTIVITY) or (event.type == Events.JINCAFE),
                            f'It should only return weekly activities and weekends, '
                            f'type of this event: {event.get_type_display()}')

    def test_it_should_not_return_passed_events(self):
        # Operate
        events = get_public_and_jincafe_events()

        # Check
        self.assertIsNotNone(events)
        for event in events:
            self.assertFalse('past event' in event.name,
                             f'It should not include events from the past:'
                             f'startDate = {event.startDate}'
                             f', endDate = {event.endDate}')
