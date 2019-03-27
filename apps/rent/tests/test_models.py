import decimal
import random
from datetime import date, datetime

from django.test import TestCase

from apps.agenda.models import Event
from apps.home.constants import Events
from apps.rent.models import Reservation, Pricing, get_prices


# TODO misschien in forms testen, maar als er nieuwe prijs is, dat de oude contracten nog aan hun prijs hangen

class PricingTestCase(TestCase):

    @staticmethod
    def random_price():
        return decimal.Decimal(random.randrange(1, 100000)) / 100

    def create_pricing(self):
        return Pricing.objects.create(perPersonPerDay=self.random_price(),
                                      dailyMinimum=self.random_price(),
                                      electricitykWh=self.random_price(),
                                      waterSqM=self.random_price(),
                                      gasPerDay=self.random_price(),
                                      deposit=self.random_price(),
                                      )

    def test_str_method(self):
        # Build
        pricing = self.create_pricing()
        now = datetime.now()
        pricing.pricesSetOn = now

        # Operate
        pricingString = str(pricing)

        # Check
        self.assertEqual(pricingString,
                         'Pricing (' + str(now) + ')',
                         'String method should return something readable')

    def test_pricesSetOn_being_set_automatically_at_create(self):
        # Build
        pricing = self.create_pricing()

        # Operate
        pricesSetOn = pricing.pricesSetOn

        # Check
        self.assertIsNotNone(pricesSetOn, 'Field pricesSetOn should be generated automatically')

    def test_pricesSetOn_not_changed_when_modifying_object(self):
        # Build
        pricing = self.create_pricing()

        # Operate
        createdAt = pricing.pricesSetOn
        pricing.pricesSetOn = datetime.now()
        afterModification = Pricing.objects.first().pricesSetOn

        # Check
        self.assertEqual(createdAt, afterModification, 'Modification of Pricing should not alter pricesSetOn')

    def test_get_prices_method_returning_the_latest_prices(self):
        # Build
        for x in range(0, 10):
            self.create_pricing()

        # Operate
        latest_price = get_prices()

        # Check
        self.assertEqual(latest_price,
                         Pricing.objects.order_by('-pricesSetOn').first(),
                         'get_prices() should return the latest price')

        # Extra Build
        latest_added = self.create_pricing()

        # Extra Operate
        latest_price = get_prices()

        # Extra Check
        self.assertEqual(latest_price.id,
                         latest_added.id,
                         'get_prices() should return the latest added price')

    def test_get_prices_method_returning_everything_zero_when_database_is_empty(self):
        # Operate
        pricing = get_prices()

        # Check
        self.assertIsNone(Pricing.objects.first(), 'Database should be empty for this test')
        self.assertEqual(pricing.perPersonPerDay, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.dailyMinimum, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.electricitykWh, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.waterSqM, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.gasPerDay, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')
        self.assertEqual(pricing.deposit, 0,
                         'With if the database is empty, get_prices() should have all prices set to zero')

    # todo when mails and users are developed
    # def test_get_prices_method_send_mail_when_calling_and_database_is_empty(self):
    # self.assertTrue(False, 'Todo when mails and users are developed')
        # also check that the recipients are correct in other test
        # Build

        # Operate

        # Check

    def test_get_prices_method_not_creating_pricing_when_database_empty(self):
        # Operate
        get_prices()

        # Check
        self.assertIsNone(Pricing.objects.first())


class ReservationTestCase(TestCase):
    a_valid_event = None
    minimal_valid_reservation = None

    def setUp(self):
        self.a_valid_event = Event.objects.create(startDate=date(2019, 7, 1),
                                                  endDate=date(2019, 7, 11),
                                                  type=Events.RENTAL)

        self.minimal_valid_reservation = Reservation.objects.create(groupName='De Bosvogels',
                                                                    town='Grobbendonk',
                                                                    email='info@bosvogels.be',
                                                                    phoneNr='0032412345678',
                                                                    period=self.a_valid_event,
                                                                    bankAccountNumber='BE12 1234 5678 9876',
                                                                    pricing=Pricing.objects.create(
                                                                        perPersonPerDay=10,
                                                                        dailyMinimum=10,
                                                                        electricitykWh=10,
                                                                        gasPerDay=10,
                                                                        waterSqM=10,
                                                                        deposit=10,
                                                                    ),
                                                                    numberOfPeople=20)

    def test_str_method(self):
        # Check
        self.assertEqual(str(self.minimal_valid_reservation),
                         'De Bosvogels (Grobbendonk), 2019-07-01 - 2019-07-11',
                         'String method should display something meaningful')

    def test_str_method_no_period(self):
        # Build
        reservation = self.minimal_valid_reservation

        # Operate
        reservation.period = None

        # Check
        self.assertEqual(str(reservation),
                         'De Bosvogels (Grobbendonk)',
                         'String method should display something meaningful')

    def test_required_fields(self):
        # Check
        self.minimal_valid_reservation.full_clean()

    def test_event_deleted_when_reservation_deleted(self):
        # Operate
        Reservation.objects.first().delete()

        # Check
        self.assertEqual(Event.objects.all().count(),
                         0,
                         'When a reservation is deleted, the corresponding event should be deleted')

    def test_reservation_should_persist_if_event_gets_deleted(self):
        # Operate
        Event.objects.first().delete()

        # Check
        self.assertEqual(Reservation.objects.all().count(),
                         1,
                         'When an event is somehow deleted, the corresponding reservation should persist')
        self.assertIsNone(Reservation.objects.first().period,
                          'The period should be set to null in the database')
