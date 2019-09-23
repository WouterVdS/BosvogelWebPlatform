from datetime import datetime, timedelta, time, date

from django.test import TestCase, Client
from django.urls import reverse

from apps.agenda.models import Event
from apps.home.constants import Takken, Events
from apps.place.models import Place


class TakviewVergaderingenTestCase(TestCase):

    def test_only_the_correct_event_types_are_shown(self):
        for event_type in Events.EVENT_TYPES:
            # Build
            eventname = 'Test event name milqsjdmlr'
            event = Event.objects.create(
                name=eventname,
                startDate=datetime.today(),
                type=event_type[0],
                tak=Takken.KAPOENEN
            )

            # Operate
            response = Client().get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
            content = str(response.content)

            # Check
            self.assertEqual(1, Event.objects.count(), 'There should not remain events from previous tests')
            if event_type[0] in [Events.PUBLIC_ACTIVITY, Events.WEEKLY_ACTIVITY, Events.WEEKEND]:
                self.assertTrue(eventname in content,
                                f'Events of type {event_type[1]} should be shown')
            else:
                self.assertFalse(eventname in content,
                                 f'Events of type {event_type[1]} should not be shown')
            event.delete()

    def test_order_of_events_is_correct(self):
        # Build
        today = datetime.today()
        two_days_ago = today - timedelta(days=2)
        yesterday = today - timedelta(days=1)
        tomorrow = today + timedelta(days=1)

        now = datetime.now().time()
        two_hours_ago = (datetime.now() - timedelta(hours=2)).time()
        one_hour_ago = (datetime.now() - timedelta(hours=1)).time()
        one_hour_from_now = (datetime.now() + timedelta(hours=1)).time()

        Event.objects.create(
            name='Event number 0',
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN,
            startDate=two_days_ago,
            startTime=now,
            endDate=today,
            endTime=two_hours_ago
        )
        Event.objects.create(
            name='Event number 1',
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN,
            startDate=yesterday,
            startTime=now,
            endDate=tomorrow,
            endTime=now
        )
        Event.objects.create(
            name='Event number 2',
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN,
            startDate=today,
            startTime=two_hours_ago,
            endDate=today,
            endTime=one_hour_ago
        )
        Event.objects.create(
            name='Event number 3',
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN,
            startDate=today,
            startTime=one_hour_ago,
            endDate=today,
            endTime=one_hour_from_now
        )
        Event.objects.create(
            name='Event number 4',
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN,
            startDate=today,
            startTime=one_hour_from_now,
            endDate=tomorrow,
            endTime=now
        )

        Event.objects.create(
            name='Event number 5',
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN,
            startDate=tomorrow,
            startTime=two_hours_ago,
            endDate=tomorrow,
            endTime=one_hour_from_now
        )

        # Operate
        response = Client().get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        prev_index = 0
        for x in range(5):
            index = content.index(f'Event number {x}')
            self.assertTrue(index > prev_index,
                            'The events should be displayed in the correct order')
            prev_index = index

    def test_an_empty_inbox_message_is_displayed_when_no_events_are_ready_to_be_shown(self):
        # Operate
        response = Client().get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertTrue('Momenteel nog geen vergaderingen gepland!' in content,
                        'When no events are planned, an empty inbox message should be shown')

    def test_check_if_required_data_is_displayed(self):
        # Build
        testplace = Place.objects.create(
            name='De Rimboe',
            country='België',
            zipcode='2280',
            city='Grobbendonk',
            street_and_number='Kremersgat 2'
        )
        testevent = Event.objects.create(
            name='TestName',
            place=testplace,
            startDate=datetime.today(),
            endDate=datetime.today() + timedelta(days=1),
            startTime=time(hour=14),
            endTime=time(hour=16, minute=30),
            description='This is the description',
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = Client().get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertTrue(testevent.name in content,
                        'The name should be displayed for an event')
        self.assertTrue(str(testevent.place) in content,
                        'The location should be displayed for an event')
        self.assertTrue(testevent.description in content,
                        'The description should be displayed for an event')
        self.assertTrue(str(testevent.startDate.day) in content,
                        'The start date should be displayed for an event')
        self.assertTrue(str(testevent.startDate.year) in content,
                        'The start date should be displayed for an event')
        self.assertTrue(str(testevent.endDate.day) in content,
                        'The end date should be displayed for an event')
        self.assertTrue(str(testevent.endDate.year) in content,
                        'The end date should be displayed for an event')
        self.assertTrue('14:00' in content,
                        'The start time should be displayed for an event')
        self.assertTrue('16:30' in content,
                        'The end time should be displayed for an event')

    def test_the_date_should_be_formatted_correct(self):
        # Build
        next_year = (datetime.now().year + 1)
        Event.objects.create(
            startDate=date(next_year, 1, 1),
            endDate=date(next_year, 1, 2),
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = Client().get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)
        expected = f'1 januari {next_year} - 2 januari {next_year}'

        # Check
        self.assertTrue(expected in content,
                        f'The date should be displayed correctly. Expected: "{expected}". Got: {content}')

    def test_the_date_should_be_formatted_correct_if_no_enddate_is_provided(self):
        # Build
        next_year = (datetime.now().year + 1)
        Event.objects.create(
            startDate=date(next_year, 1, 1),
            endDate=date(next_year, 1, 2),
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = Client().get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)
        expected = f'1 januari {next_year} - 2 januari {next_year}'

        # Check
        self.assertTrue(expected in content,
                        f'The date should be displayed correctly. Expected: "{expected}". Got: {content}')

    def test_only_furure_or_events_for_this_day_should_be_displayed(self):
        # Build
        now = date.today()
        Event.objects.create(
            name='ditmagjenietzien',
            startDate=now - timedelta(days=1),
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = Client().get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertTrue('ditmagjenietzien' not in content,
                        'Past events should not be displayed')
