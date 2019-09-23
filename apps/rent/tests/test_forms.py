import logging
from datetime import datetime, date

from django.test import TestCase

from apps.agenda.models import Event
from apps.home.constants import Events
from apps.rent.forms import ReservationForm, PricingForm
from apps.rent.models import Pricing


class ReservationFormTestCase(TestCase):

    def setUp(self):
        self.formData = {
            'groupName': 'Testgroup',
            'town': 'Testtown',
            'email': 'test@test.test',
            'phoneNr': '0471111111',
            'bankAccountNumber': 'BE24 2424 2424 2424',
            'startDate': '01-07-' + str(datetime.now().year + 1),
            'endDate': '10-07-' + str(datetime.now().year + 1),
            'numberOfPeople': '50',
            'comments': 'blablabla',
        }

    def test_valid_form(self):
        # Build
        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertTrue(valid, 'This form should be a valid one')

    def test_required_fields_empty_validation(self):
        # Build
        fields = [
            'groupName',
            'town',
            'email',
            'phoneNr',
            'bankAccountNumber',
            'numberOfPeople',
        ]

        for field in fields:
            invalidData = self.formData.copy()
            invalidData[field] = ''
            form = ReservationForm(invalidData)

            # Operate
            valid = form.is_valid()
            errors = form.errors

            # Check
            self.assertFalse(valid, f'Form with {field} empty should not validate')
            self.assertEqual(errors,
                             {field: ['Dit veld is verplicht.']},
                             f'Field {field} should be required')

    def test_comment_field_present(self):
        # Build
        self.formData['comments'] = 'testcomment'
        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertTrue(valid, 'Form should come with optional comment section')

    def test_validation_startdate_in_past(self):
        # Build
        self.formData['startDate'] = '01-07-' + str(datetime.now().year - 1)
        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertFalse(valid, 'StartDate in the past should not validate')

    def test_validation_startdate_not_in_summer(self):
        notSummerMonths = [1, 2, 3, 4, 5, 10, 11, 12]
        for month in notSummerMonths:
            # Build
            self.formData['startDate'] = f'01-{month}-' + str(datetime.now().year + 1)
            form = ReservationForm(self.formData)

            # Operate
            valid = form.is_valid()

            # Check
            self.assertFalse(valid,
                             f'StartDate in the month number {month} should not validate as it is not in the summer')

    def test_validation_enddate_in_past(self):
        # Build
        self.formData['endDate'] = '01-07-' + str(datetime.now().year - 1)
        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertFalse(valid, 'EndDate in the past should not validate')

    def test_validation_enddate_not_in_summer(self):
        notSummerMonths = [1, 2, 3, 4, 5, 10, 11, 12]
        for month in notSummerMonths:
            # Build
            self.formData['endDate'] = f'01-{month}-' + str(datetime.now().year + 1)
            form = ReservationForm(self.formData)

            # Operate
            valid = form.is_valid()

            # Check
            self.assertFalse(valid,
                             f'EndDate in the month number {month} should not validate as it is not in the summer')

    def test_validation_enddate_before_startdate(self):
        # Build
        self.formData['startDate'] = '01-08-' + str(datetime.now().year + 1)
        self.formData['endDate'] = '01-07-' + str(datetime.now().year + 1)
        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()
        errors = form.errors

        # Check
        self.assertFalse(valid, 'Form with endDate before startDate should not validate')
        self.assertEqual(errors,
                         {'__all__': ['De einddatum moet na de startdatum komen']},
                         'The correct error message should be displayed')

    def test_validation_startdate_none(self):
        # Build
        # noinspection PyTypeChecker
        self.formData['startDate'] = None
        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertFalse(valid, 'Form with startDate None should not validate')

    def test_validation_enddate_none(self):
        # Build
        # noinspection PyTypeChecker
        self.formData['endDate'] = None
        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertFalse(valid, 'Form with endDate None should not validate')

    def test_period_valid(self):
        # Build
        nextYear = datetime.now().year + 1
        Event.objects.create(
            name='Testrentalevent',
            startDate=date(nextYear, 7, 1),
            endDate=date(nextYear, 7, 30),
            type=Events.RENTAL
        )

        toRentStartDate = f'10-08-{nextYear}'
        toRentEndDate = f'20-08-{nextYear}'

        self.formData['startDate'] = toRentStartDate
        self.formData['endDate'] = toRentEndDate

        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertTrue(valid,
                        f'No validation error should be thrown when it is able to rent, error: {form.errors}')

    def test_period_valid_between_two_others(self):
        # Build
        nextYear = datetime.now().year + 1
        Event.objects.create(
            name='Testrentalevent',
            startDate=date(nextYear, 7, 1),
            endDate=date(nextYear, 7, 10),
            type=Events.RENTAL
        )
        Event.objects.create(
            name='Testrentalevent',
            startDate=date(nextYear, 7, 20),
            endDate=date(nextYear, 7, 30),
            type=Events.RENTAL
        )

        toRentStartDate = f'10-07-{nextYear}'
        toRentEndDate = f'20-07-{nextYear}'

        self.formData['startDate'] = toRentStartDate
        self.formData['endDate'] = toRentEndDate

        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertTrue(valid, 'Ending/starting different rent periods on the same day should be possible')

    def test_period_invalid_full_overlap(self):
        # Build
        nextYear = datetime.now().year + 1
        Event.objects.create(
            name='Testrentalevent',
            startDate=date(nextYear, 7, 1),
            endDate=date(nextYear, 7, 30),
            type=Events.RENTAL
        )

        toRentStartDate = f'10-07-{nextYear}'
        toRentEndDate = f'20-07-{nextYear}'

        self.formData['startDate'] = toRentStartDate
        self.formData['endDate'] = toRentEndDate

        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()
        errors = form.errors

        # Check
        self.assertFalse(valid, 'A validation error should be thrown when rent period is not available')
        self.assertEqual(errors,
                         {'__all__': ['Deze periode is niet volledig vrij om te huren']},
                         'A validation error should be thrown when renting in that period is not possible')

    def test_period_invalid_exactly_the_same(self):
        # Build
        nextYear = datetime.now().year + 1
        Event.objects.create(
            name='Testrentalevent',
            startDate=date(nextYear, 7, 1),
            endDate=date(nextYear, 7, 30),
            type=Events.RENTAL
        )

        toRentStartDate = f'1-07-{nextYear}'
        toRentEndDate = f'30-07-{nextYear}'

        self.formData['startDate'] = toRentStartDate
        self.formData['endDate'] = toRentEndDate

        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()
        errors = form.errors

        # Check
        self.assertFalse(valid, 'A validation error should be thrown when rent period is not available')
        self.assertEqual(errors,
                         {'__all__': ['Deze periode is niet volledig vrij om te huren']},
                         'A validation error should be thrown when renting in that period is not possible')

    def test_period_invalid_full_embrace(self):
        # Build
        nextYear = datetime.now().year + 1
        Event.objects.create(
            name='Testrentalevent',
            startDate=date(nextYear, 7, 12),
            endDate=date(nextYear, 7, 15),
            type=Events.RENTAL
        )

        toRentStartDate = f'10-07-{nextYear}'
        torentEndDate = f'20-07-{nextYear}'

        self.formData['startDate'] = toRentStartDate
        self.formData['endDate'] = torentEndDate

        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()
        errors = form.errors

        # Check
        self.assertFalse(valid, 'A validation error should be thrown when rent period is not available')
        self.assertEqual(errors,
                         {'__all__': ['Deze periode is niet volledig vrij om te huren']},
                         'A validation error should be thrown when renting in that period is not possible')

    def test_period_invalid_begin_overlap(self):
        # Build
        nextYear = datetime.now().year + 1
        Event.objects.create(
            name='Testrentalevent',
            startDate=date(nextYear, 7, 1),
            endDate=date(nextYear, 7, 15),
            type=Events.RENTAL
        )

        toRentStartDate = f'10-07-{nextYear}'
        torentEndDate = f'20-07-{nextYear}'

        self.formData['startDate'] = toRentStartDate
        self.formData['endDate'] = torentEndDate

        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()
        errors = form.errors

        # Check
        self.assertFalse(valid, 'A validation error should be thrown when rent period is not available')
        self.assertEqual(errors,
                         {'__all__': ['Deze periode is niet volledig vrij om te huren']},
                         'A validation error should be thrown when renting in that period is not possible')

    def test_period_invalid_end_overlap(self):
        # Build
        nextYear = datetime.now().year + 1
        Event.objects.create(
            name='Testrentalevent',
            startDate=date(nextYear, 7, 29),
            endDate=date(nextYear, 8, 10),
            type=Events.RENTAL
        )

        toRentStartDate = f'20-07-{nextYear}'
        torentEndDate = f'30-07-{nextYear}'

        self.formData['startDate'] = toRentStartDate
        self.formData['endDate'] = torentEndDate

        form = ReservationForm(self.formData)

        # Operate
        valid = form.is_valid()
        errors = form.errors

        # Check
        self.assertFalse(valid, 'A validation error should be thrown when rent period is not available')
        self.assertEqual(errors,
                         {'__all__': ['Deze periode is niet volledig vrij om te huren']},
                         'A validation error should be thrown when renting in that period is not possible')


class PricingFormTestCase(TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.formData = {
            'perPersonPerDay': '10',
            'dailyMinimum': '10',
            'electricitykWh': '10',
            'waterSqM': '10',
            'gasPerDay': '10',
            'deposit': '10',
        }

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_valid_form(self):
        # Build
        form = PricingForm(self.formData)

        # Operate
        valid = form.is_valid()

        # Check
        self.assertTrue(valid, 'This form should be a valid one')

    def test_required_fields_empty(self):
        fields = [
            'perPersonPerDay',
            'dailyMinimum',
            'electricitykWh',
            'waterSqM',
            'gasPerDay',
            'deposit',
        ]
        for field in fields:
            invalidData = self.formData.copy()
            invalidData[field] = ''
            form = PricingForm(invalidData)
            self.assertFalse(form.is_valid(), f'Form with {field} empty should not validate')
            self.assertEqual(form.errors,
                             {field: ['Dit veld is verplicht.']},
                             f'Field {field} should be required')

    def test_validation_when_pricing_changed(self):
        # Build
        Pricing.objects.create(
            perPersonPerDay=10.10,
            dailyMinimum=10.10,
            electricitykWh=10.10,
            waterSqM=10.10,
            gasPerDay=10.10,
            deposit=10.10,
        )
        form = PricingForm({
            'perPersonPerDay': '11.10',
            'dailyMinimum': '10.10',
            'electricitykWh': '10.10',
            'waterSqM': '10.10',
            'gasPerDay': '10.10',
            'deposit': '10.10',
        })

        # Operate
        valid = form.is_valid()

        # Check
        self.assertTrue(valid, 'When a price changed, the form shoud be valid')

    def test_validation_when_pricing_did_not_change(self):
        # Build
        Pricing.objects.create(
            perPersonPerDay=10.10,
            dailyMinimum=10.10,
            electricitykWh=10.10,
            waterSqM=10.10,
            gasPerDay=10.10,
            deposit=10.10,
        )
        form = PricingForm({
            'perPersonPerDay': '10.10',
            'dailyMinimum': '10.10',
            'electricitykWh': '10.10',
            'waterSqM': '10.10',
            'gasPerDay': '10.10',
            'deposit': '10.10',
        })

        # Operate
        valid = form.is_valid()
        errors = form.errors

        # Check
        self.assertFalse(valid, 'A validation error should be thrown when prices are the same')
        self.assertEqual(errors,
                         {'__all__': ['Geen verschil met de vorige tarieven.']},
                         'A validation error should be thrown when prices are the same')
