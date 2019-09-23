from datetime import datetime, date, time

from django.test import Client, TestCase
from django.urls import reverse

from apps.agenda.models import Event
from apps.home.constants import Events, Takken
from apps.place.models import Place


class IndexViewTestCase(TestCase):

    def test_index_response_code(self):
        # Operate
        response = Client().get(reverse('agenda:index'))

        # Check
        self.assertEqual(response.status_code, 200, 'Index should have a HTTP OK response')

    def test_order_of_displayed_events_by_date(self):
        # Build public events
        year = datetime.now().year + 1
        month = datetime.now().month

        Event.objects.create(
            name='Event with id 1',
            type=Events.PUBLIC_ACTIVITY,
            startDate=date(year, month, 2)
        )
        Event.objects.create(
            name='Event with id 2',
            type=Events.PUBLIC_ACTIVITY,
            startDate=date(year, month, 3)
        )
        Event.objects.create(
            name='Event with id 0',
            type=Events.PUBLIC_ACTIVITY,
            startDate=date(year, month, 1)
        )

        # Build weekly meetings
        Event.objects.create(
            name='Event with id 4',
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year, month, 5)
        )
        Event.objects.create(
            name='Event with id 3',
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year, month, 4)
        )

        Event.objects.create(
            name='Event with id 5',
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year, month, 6)
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        index = 0
        for x in range(Event.objects.count()):
            new_index = content.find(f'Event with id {x}')
            self.assertTrue(new_index > index, 'First event to follow should be displayed on top')
            index = new_index
        self.assertFalse('Testevent' in content, 'It should not display passed events')

    def test_order_of_displayed_events_by_time(self):
        # Build public events
        year = datetime.now().year + 1
        month = datetime.now().month
        day = 2

        Event.objects.create(
            name='Event with id 1',
            type=Events.PUBLIC_ACTIVITY,
            startDate=date(year, month, day),
            startTime=time(10, 0, 0)
        )
        Event.objects.create(
            name='Event with id 2',
            type=Events.PUBLIC_ACTIVITY,
            startDate=date(year, month, day),
            startTime=time(11, 0, 0)
        )
        Event.objects.create(
            name='Event with id 0',
            type=Events.PUBLIC_ACTIVITY,
            startDate=date(year, month, day),
            startTime=time(9, 0, 0)
        )

        # Build weekly meetings
        Event.objects.create(
            name='Event with id 4',
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year, month, day),
            startTime=time(10, 0, 0)
        )
        Event.objects.create(
            name='Event with id 3',
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year, month, day),
            startTime=time(9, 0, 0)
        )

        Event.objects.create(
            name='Event with id 5',
            type=Events.WEEKLY_ACTIVITY,
            startDate=date(year, month, day),
            startTime=time(11, 0, 0)
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        index = 0
        for x in range(Event.objects.count()):
            new_index = content.find(f'Event with id {x}')
            self.assertTrue(new_index > index, 'First event to follow should be displayed on top')
            index = new_index
        self.assertFalse('Testevent' in content, 'It should not display passed events')

    def test_it_should_not_display_passed_events(self):
        # Build
        year = datetime.now().year
        month = datetime.now().month
        Event.objects.create(
            name='Past event',
            startDate=date(year, month - 1, 1),
            type=Events.WEEKLY_ACTIVITY
        )
        Event.objects.create(
            name='Past event',
            startDate=date(year, month - 1, 1),
            type=Events.PUBLIC_ACTIVITY
        )
        hour = datetime.now().hour
        Event.objects.create(
            name='Event currently busy timewise',
            startDate=datetime.now().date(),
            startTime=time(max(0, hour - 1), 0, 0),
            endTime=time(min(23, hour + 1), 0, 0),
            type=Events.PUBLIC_ACTIVITY
        )
        day = datetime.now().day
        Event.objects.create(
            name='Event currently busy datewise',
            startDate=date(year, month - 1, day),
            endDate=date(year, month, day + 2),
            type=Events.PUBLIC_ACTIVITY
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertFalse('Past event' in content, 'It should not display passed events')
        self.assertTrue('Event currently busy timewise' in content, 'It should show events which are currently busy')
        self.assertTrue('Event currently busy datewise' in content, 'It should show events which are currently busy')

    def test_it_should_display_relevant_information_for_general_events(self):
        # Build
        year = datetime.now().year + 1
        Event.objects.create(
            name='Eventname',
            place=Place.objects.create(name='Testplace'),
            startDate=date(year, 1, 1),
            endDate=date(year, 2, 2),
            startTime=time(12, 0, 0),
            endTime=time(15, 0, 0),
            description='Testdescription',
            type=Events.PUBLIC_ACTIVITY
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertTrue('Eventname' in content, 'It should display the eventname')
        self.assertTrue('Testplace' in content, 'It should display the place')
        self.assertTrue(f'1 januari {year}' in content, 'It should display the start date')
        self.assertTrue(f'2 februari {year}' in content, 'It should display the end date')
        self.assertTrue('12:00' in content, 'It should display the start time')
        self.assertTrue('15:00' in content, 'It should display the end time')
        self.assertTrue('Testdescription' in content, 'It should display the description')

    def test_it_should_display_relevant_information_for_weekly_meetings(self):
        # Build
        year = datetime.now().year + 1
        Event.objects.create(
            name='Eventname',
            place=Place.objects.create(name='Testplace'),
            startDate=date(year, 1, 1),
            endDate=date(year, 2, 2),
            startTime=time(12, 0, 0),
            endTime=time(15, 0, 0),
            description='Testdescription',
            type=Events.WEEKLY_ACTIVITY,
            tak=Takken.KAPOENEN
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertTrue('Eventname' in content, 'It should display the eventname')
        self.assertTrue('Testplace' in content, 'It should display the place')
        self.assertTrue(f'1 januari {year}' in content, 'It should display the start date')
        self.assertTrue(f'2 februari {year}' in content, 'It should display the end date')
        self.assertTrue('12:00' in content, 'It should display the start time')
        self.assertTrue('15:00' in content, 'It should display the end time')
        self.assertTrue('Testdescription' in content, 'It should display the description')
        self.assertTrue('Kapoenen' in content, 'It should display the tak')

    def test_it_should_never_display_none(self):
        # Build
        Event.objects.create(
            type=Events.PUBLIC_ACTIVITY,
            startDate=datetime.now()
        )
        Event.objects.create(
            type=Events.WEEKLY_ACTIVITY,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)
        # Check
        self.assertFalse('None' in content,
                         'When "None" is displayed, it is most likely an error')

    def test_it_should_display_weekly_activities(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.WEEKLY_ACTIVITY,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertTrue('Testevent' in content,
                        'Public events should be displayed')

    def test_it_should_display_public_activities(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.PUBLIC_ACTIVITY,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertTrue('Testevent' in content,
                        'Public events should be displayed')

    def test_it_should_display_weekends(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.WEEKEND,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertTrue('Testevent' in content,
                        'Weekends should be displayed')

    def test_it_should_display_jincafes(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.JINCAFE,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertTrue('Testevent' in content,
                        'Jincafé\'s should be displayed')

    def test_it_should_not_display_rental_events(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.RENTAL,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertFalse('Testevent' in content,
                         'Rental events should not be displayed')

    def test_it_should_not_display_leader_activities(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.LEADER_ACTIVITY,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertFalse('Testevent' in content,
                         'Leader activities should not be displayed')

    def test_it_should_not_display_camps(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.CAMP,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertFalse('Testevent' in content,
                         'Camps should not be displayed')

    def test_it_should_not_display_workdays(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.WORKDAY,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertFalse('Testevent' in content,
                         'Workdays should not be displayed')

    def test_it_should_not_display_groupmeetings(self):
        # Build
        Event.objects.create(
            name='Testevent',
            type=Events.GROUPMEETING,
            startDate=datetime.now()
        )

        # Operate
        response = Client().get(reverse('agenda:index'))
        content = str(response.content)

        # Check
        self.assertFalse('Testevent' in content,
                         'Groupmeetings should not be displayed')
