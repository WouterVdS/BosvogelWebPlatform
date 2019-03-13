from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.agenda.models import Event
from apps.home.constants import Events
from apps.rent.models import RentReservation


class RentReservationTestCase(TestCase):
    a_valid_event = None
    minimal_valid_reservation = None

    def setUp(self):
        self.a_valid_event = Event.objects.create(startDate=date(2019, 7, 1),
                                                  endDate=date(2019, 7, 11),
                                                  type=Events.RENTAL)

        self.minimal_valid_reservation = RentReservation.objects.create(groupName='De Bosvogels',
                                                                        town='Grobbendonk',
                                                                        email='info@bosvogels.be',
                                                                        phoneNr='0032412345678',
                                                                        period=self.a_valid_event,
                                                                        bankAccountNumber='BE12 1234 5678 9876',
                                                                        numberOfPeople=20)

    def test_str_method(self):
        # Check
        self.assertEqual(str(self.minimal_valid_reservation),
                         'De Bosvogels (Grobbendonk), 2019-07-01 - 2019-07-11',
                         'String method should display something meaningful')

    def test_required_fields(self):
        # Check
        self.minimal_valid_reservation.full_clean()

    def test_validation_of_international_phoneNr(self):
        # Build
        reservation = self.minimal_valid_reservation

        reservation.phoneNr = '0477556655'

        # Operate
        with self.assertRaises(ValidationError) as context:
            reservation.full_clean()

        # Check
        self.assertTrue('beginnen met 0032' in str(context.exception),
                        'But it is: ' + str(context.exception))

    def test_validation_of_bankAccountNumber(self):
        # Build
        reservation = self.minimal_valid_reservation
        reservation.bankAccountNumber = 'BE2144547wrong'

        # Operate
        with self.assertRaises(ValidationError) as context:
            reservation.full_clean()

        # Check
        self.assertTrue('Rekeningnummer moet in het volgende formaat' in str(context.exception),
                        'But it is: ' + str(context.exception))

    def test_event_deleted_when_reservation_deleted(self):
        # Operate
        RentReservation.objects.first().delete()

        # Check
        self.assertEqual(Event.objects.all().count(),
                         0,
                         'When a reservation is deleted, the corresponding event should be deleted')

    def test_reservation_should_persist_if_event_gets_deleted(self):
        # Operate
        Event.objects.first().delete()

        # Check
        self.assertEqual(RentReservation.objects.all().count(),
                         1,
                         'When an event is somehow deleted, the corresponding reservation should persist')
        self.assertIsNone(RentReservation.objects.first().period,
                          'The period should be set to null in the database')
