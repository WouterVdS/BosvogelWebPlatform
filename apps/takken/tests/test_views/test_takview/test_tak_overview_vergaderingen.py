from datetime import datetime, timedelta, time, date

from django.test import TestCase
from django.urls import reverse

from apps.agenda.models import Event
from apps.home.constants import Takken, Events
from apps.home.models import Werkjaar, get_workyear
from apps.place.models import Place


class TakOverviewVergaderingenTestCase(TestCase):

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
            response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
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

        now = datetime(2019, 1, 1, 12, 0, 0)
        two_hours_ago = (now - timedelta(hours=2)).time()
        one_hour_ago = (now - timedelta(hours=1)).time()
        one_hour_from_now = (now + timedelta(hours=1)).time()

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
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
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
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertTrue('Momenteel nog geen vergaderingen gepland!' in content,
                        'When no events are planned, an empty inbox message should be shown')

    def test_None_is_never_displayed(self):
        # Build
        Event.objects.create(
            startDate=datetime.today(),
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertFalse('None' in content,
                         f'"None" should not be displayed, but it is displayed: \n\n{content}')

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
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
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
        start_date = date(next_year, 1, 1)
        while start_date.weekday() != 5:
            start_date = start_date + timedelta(days=1)
        Event.objects.create(
            startDate=start_date,
            endDate=start_date + timedelta(days=1),
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        expected = f'Zaterdag {start_date.day} januari {next_year} - zondag {start_date.day + 1} januari {next_year}'

        # Check
        self.assertTrue(expected in content,
                        f'The date should be displayed correctly. Expected: "{expected}". Got: \n\n{content}')

    def test_the_date_should_be_formatted_correct_if_no_enddate_is_provided(self):
        # Build
        next_year = (datetime.now().year + 1)
        Event.objects.create(
            startDate=date(next_year, 1, 1),
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)
        expected = f'1 januari {next_year}'

        # Check
        self.assertTrue(expected in content,
                        f'The date should be displayed correctly. Expected: "{expected}". Got: \n\n{content}')

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
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertTrue('ditmagjenietzien' not in content,
                        'Past events should not be displayed')

    def test_leiding_should_not_have_vergaderingen_section(self):
        # Operate
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[8][1]]))  # leiding
        content = str(response.content)

        # Check
        self.assertTrue('Vergaderingen' not in content,
                        'The section "Vergaderingen" should not be shown/exist for leiding')

    def test_groepsleiding_should_not_have_vergaderingen_section(self):
        # Operate
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[9][1]]))  # groepsleiding
        content = str(response.content)

        # Check
        self.assertTrue('Vergaderingen' not in content,
                        'The section "Vergaderingen" should not be shown/exist for groepsleiding')

    def test_leiding_should_not_have_leiding_section(self):
        # Operate
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[8][1]]))  # leiding
        content = str(response.content)

        # Check
        self.assertTrue('>Leiding<h' not in content,
                        'The section "Leiding" should not be shown/exist for leiding')

    def test_day_of_the_week_should_be_displayed(self):
        # Build
        saturday = date.today()
        while saturday.weekday() != 5:  # pragma: no cover
            saturday = saturday + timedelta(days=1)
        sunday = date.today()
        while sunday.weekday() != 6:
            sunday = sunday + timedelta(days=1)
        Event.objects.create(
            startDate=saturday,
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )
        Event.objects.create(
            startDate=sunday,
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = self.client.get(reverse('takken:tak', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertTrue('Zaterdag' in content,
                        f'The day of the week should be displayed with meetings. Expected "Zaterdag", '
                        f'but got: \n{content}')
        self.assertTrue('Zondag' in content,
                        f'The day of the week should be displayed with meetings. Expected "Zondag", '
                        f'but got: \n{content}')

    def test_passed_events_displayed_when_accessing_all_vergaderingen(self):
        # Build
        last_week = date.today() - timedelta(weeks=1)
        name = 'Event which was past week'
        Event.objects.create(
            startDate=last_week,
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN,
            name=name
        )

        # Operate
        response = self.client.get(reverse('takken:tak_all_vergaderingen', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertTrue(name in content,
                        'When accessing all vergaderingen, the past ones should be displayed also.'
                        f'Expected an event with name "{name}",'
                        f'but got: \n\n{content}')

    def test_if_vergaderingen_for_the_next_year_are_displayed(self):
        # Build
        name = 'future event'

        current_year = get_workyear()

        Event.objects.create(
            name=name,
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN,
            startDate=date(year=current_year+1, month=9, day=20)
        )

        # Operate
        response = self.client.get(reverse('takken:tak_all_vergaderingen', args=[Takken.TAKKEN[0][1]]))  # kapoenen
        content = str(response.content)

        # Check
        self.assertTrue(name in content,
                        'Events from the next workyear should be displayed, this can be useful at the end of august')
