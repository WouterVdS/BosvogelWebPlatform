from datetime import datetime, date

from django.test import TestCase, Client
from django.urls import reverse

from apps.agenda.models import Event
from apps.home.constants import Events
from apps.rent.models import Reservation, Pricing


class ReserveTestCase(TestCase):

    def setUp(self):
        Pricing.objects.create(
            perPersonPerDay=1,
            dailyMinimum=2,
            electricitykWh=3,
            waterSqM=4,
            gasPerDay=5,
            deposit=6
        )

    def test_status_code(self):
        # Build
        response = self.client.get(reverse('rent:reserve'))

        # Operate
        status_code = response.status_code

        # Assert
        self.assertEqual(status_code, 200)

    def test_title_suffix(self):
        # Build
        response = self.client.get(reverse('rent:reserve'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<title>De Bosvogels - Reserveren</title>' in content,
                        'The correct head title should be displayed')

    def test_get_form_displayed(self):
        # Build
        response = self.client.get(reverse('rent:reserve'))

        # Operate
        content = str(response.content)

        # Check
        self.assertTrue('<form action="/verhuur/reserveren/" method="post">' in content,
                        'The reservation form should be displayed')

    def test_post_invalid_form_no_redirect(self):
        # Build
        client = Client()

        # Operate
        response = client.post(reverse('rent:reserve'), {}, follow=True)

        # Check
        self.assertEqual(response.redirect_chain,
                         [],
                         'When the form is invalid, no redirect should occur')

    def test_post_invalid_form_redisplayed(self):
        # Build
        client = Client()
        groupName = 'Invalid Form mslijzmleij'

        # Operate
        response = client.post(reverse('rent:reserve'), {
            'groupName': groupName
        })
        content = str(response.content)

        # Check
        self.assertTrue(groupName in content,
                        'When the form is invalid, it should be returned filled in')

    def test_post_invalid_form_error_messages(self):
        # Build
        client = Client()

        # Operate
        response = client.post(reverse('rent:reserve'), {})
        content = str(response.content)

        # Check
        self.assertEqual(content.count('verplicht'),
                         8,
                         'When the form is invalid, errors should be shown')

    def test_post_invalid_form_not_saved(self):
        # Build
        client = Client()

        # Operate
        client.post(reverse('rent:reserve'), {})
        reservationCount = Reservation.objects.count()

        # Check
        self.assertEqual(reservationCount,
                         0,
                         'When the form is invalid, no reservations should be saved')

    def test_post_invalid_event_not_saved(self):
        # Build
        client = Client()

        # Operate
        client.post(reverse('rent:reserve'), {})
        eventCount = Event.objects.count()

        # Check
        self.assertEqual(eventCount,
                         0,
                         'When the form is invalid, no events should be saved')

    def test_post_valid_form_saved(self):
        # Build
        client = Client()
        nextYear = datetime.now().year + 1
        testGroupName = 'Testgroup864568498'

        # Operate
        client.post(reverse('rent:reserve'), {
            'groupName': testGroupName,
            'town': 'Testtown',
            'email': 'test@test.com',
            'phoneNr': '0411111111',
            'bankAccountNumber': 'BE11 1111 1111 1111',
            'startDate': str(date(nextYear, 7, 1)),
            'endDate': str(date(nextYear, 7, 10)),
            'numberOfPeople': '50',
            'comments': 'TestComment'
        })
        reservation = Reservation.objects.first()

        # Check
        self.assertEqual(reservation.groupName,
                         testGroupName,
                         'The correct reservation should be saved')

    def test_post_valid_form_redirect(self):
        # Build
        client = Client()
        nextYear = datetime.now().year + 1

        # Operate
        response = client.post(reverse('rent:reserve'), {
            'groupName': 'Testgroup',
            'town': 'Testtown',
            'email': 'test@test.com',
            'phoneNr': '0411111111',
            'bankAccountNumber': 'BE11 1111 1111 1111',
            'startDate': str(date(nextYear, 7, 1)),
            'endDate': str(date(nextYear, 7, 10)),
            'numberOfPeople': '50',
            'comments': 'TestComment'
        }, follow=True)

        # Check
        self.assertEqual(response.redirect_chain,
                         [('/verhuur/', 302)],
                         'When the form is invalid, no redirect should occur')

    def test_post_valid_form_event_saved(self):
        # Build
        client = Client()
        nextYear = datetime.now().year + 1
        testGroupName = 'Testgroup864568498'

        # Operate
        client.post(reverse('rent:reserve'), {
            'groupName': testGroupName,
            'town': 'Testtown',
            'email': 'test@test.com',
            'phoneNr': '0411111111',
            'bankAccountNumber': 'BE11 1111 1111 1111',
            'startDate': str(date(nextYear, 7, 1)),
            'endDate': str(date(nextYear, 7, 10)),
            'numberOfPeople': '50',
            'comments': 'TestComment'
        })
        event = Event.objects.first()
        reservation = Reservation.objects.first()

        # Check
        self.assertIsNotNone(reservation.period,
                             'The event should be set as foreign key')
        self.assertEqual(event.id,
                         reservation.period_id,
                         'The correct event should be saved')

    def test_post_valid_form_correct_pricing_set(self):
        # Build
        client = Client()
        nextYear = datetime.now().year + 1
        testGroupName = 'Testgroup864568498'

        # Operate
        newPricing = Pricing.objects.create(
            perPersonPerDay=55,
            dailyMinimum=55,
            electricitykWh=55,
            waterSqM=55,
            gasPerDay=55,
            deposit=65
        )
        client.post(reverse('rent:reserve'), {
            'groupName': testGroupName,
            'town': 'Testtown',
            'email': 'test@test.com',
            'phoneNr': '0411111111',
            'bankAccountNumber': 'BE11 1111 1111 1111',
            'startDate': str(date(nextYear, 7, 1)),
            'endDate': str(date(nextYear, 7, 10)),
            'numberOfPeople': '50',
            'comments': 'TestComment'
        })
        reservation = Reservation.objects.first()

        # Check
        self.assertEqual(reservation.pricing_id,
                         newPricing.id,
                         'The correct reservation should be saved')

    def test_post_valid_form_event_dates_set_correclty(self):
        # Build
        client = Client()
        nextYear = datetime.now().year + 1
        testGroupName = 'Testgroup864568498'
        startDate = str(date(nextYear, 7, 1))
        endDate = str(date(nextYear, 7, 10))

        # Operate
        client.post(reverse('rent:reserve'), {
            'groupName': testGroupName,
            'town': 'Testtown',
            'email': 'test@test.com',
            'phoneNr': '0411111111',
            'bankAccountNumber': 'BE11 1111 1111 1111',
            'startDate': startDate,
            'endDate': endDate,
            'numberOfPeople': '50',
            'comments': 'TestComment'
        })
        event = Reservation.objects.first().period

        # Check
        self.assertEqual(str(event.startDate),
                         startDate,
                         'The correct startDate should be set')
        self.assertEqual(str(event.endDate),
                         endDate,
                         'The correct endDate should be set')

    def test_post_valid_form_event_times_set_correclty(self):
        # Build
        client = Client()
        nextYear = datetime.now().year + 1
        startDate = str(date(nextYear, 7, 1))
        endDate = str(date(nextYear, 7, 10))

        # Operate
        client.post(reverse('rent:reserve'), {
            'groupName': 'Testgroup',
            'town': 'Testtown',
            'email': 'test@test.com',
            'phoneNr': '0411111111',
            'bankAccountNumber': 'BE11 1111 1111 1111',
            'startDate': startDate,
            'endDate': endDate,
            'numberOfPeople': '50',
            'comments': 'TestComment'
        })
        event = Reservation.objects.first().period

        # Check
        self.assertEqual(event.startTime,
                         Events.DEFAULT_RENT_START_TIME,
                         'The correct startTime should be set')
        self.assertEqual(event.endTime,
                         Events.DEFAULT_RENT_ENDING_TIME,
                         'The correct endTime should be set')

    def test_post_valid_form_event_type_set_correclty(self):
        # Build
        client = Client()
        nextYear = datetime.now().year + 1

        # Operate
        client.post(reverse('rent:reserve'), {
            'groupName': 'Testgroup',
            'town': 'Testtown',
            'email': 'test@test.com',
            'phoneNr': '0411111111',
            'bankAccountNumber': 'BE11 1111 1111 1111',
            'startDate': str(date(nextYear, 7, 1)),
            'endDate': str(date(nextYear, 7, 10)),
            'numberOfPeople': '50',
            'comments': 'TestComment'
        })
        event = Event.objects.first()

        # Check
        self.assertEqual(event.type,
                         Events.RENTAL,
                         'The correct eventtype should be set')

    def test_post_valid_form_event_name_set_correclty(self):
        # Build
        client = Client()
        nextYear = datetime.now().year + 1
        testGroupName = 'Testgroup864568498'

        # Operate
        client.post(reverse('rent:reserve'), {
            'groupName': testGroupName,
            'town': 'Testtown',
            'email': 'test@test.com',
            'phoneNr': '0411111111',
            'bankAccountNumber': 'BE11 1111 1111 1111',
            'startDate': str(date(nextYear, 7, 1)),
            'endDate': str(date(nextYear, 7, 10)),
            'numberOfPeople': '50',
            'comments': 'TestComment'
        })
        event = Event.objects.first()

        # Check
        self.assertEqual(event.name,
                         f'Verhuur - {testGroupName}',
                         'The correct eventname should be set')

    # todo add more tests