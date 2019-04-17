import logging
from datetime import date

from django.test import TestCase

from apps.home.models import Werkjaar, get_yeartheme_logo_path


class WerkjaarTestCase(TestCase):

    first_year = 2000
    some_year = 2010
    last_year = 2020

    def setUp(self):
        logging.disable(logging.CRITICAL)
        for x in range(self.first_year, self.last_year + 1):
            Werkjaar.objects.create(year=x)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_str_method(self):
        self.assertEqual(str(Werkjaar.objects.get(year=self.some_year)), '2010 - 2011',
                         'String method should display the correct workyear')
        self.assertNotEqual(str(Werkjaar.objects.get(year=self.some_year - 1)), '2010 - 2011',
                            'String method should display the correct workyear')
        self.assertNotEqual(str(Werkjaar.objects.get(year=self.some_year + 1)), '2010 - 2011',
                            'String method should display the correct workyear')

    def test_ordering(self):
        self.assertEqual(Werkjaar.objects.first().year, self.last_year,
                         'Most recent werkjaar should be the first when queried')

    def test_current_year_aug_31(self):
        # Build
        now = date(2010, 8, 31)

        # Operate
        cy = Werkjaar.objects.current_year(now)

        # Check
        self.assertEqual(cy.year, 2009, f'{now} should be in workyear {now.year - 1} - {now.year}')

    def test_current_year_sept_1(self):
        # Build
        now = date(2010, 9, 1)

        # Operate
        cy = Werkjaar.objects.current_year(now)

        # Check
        self.assertEqual(cy.year, 2010, f'{now} should be in workyear {now.year} - {now.year + 1}')

    def test_last_year_aug_31(self):
        # Build
        now = date(2010, 8, 31)

        # Operate
        ly = Werkjaar.objects.last_year(now)

        # Check
        self.assertEqual(ly.year, 2008, f'The workyear before {now} should be 2008 - 2009')

    def test_last_year_sept_1(self):
        # Build
        now = date(2010, 9, 1)

        # Operate
        ly = Werkjaar.objects.last_year(now)

        # Check
        self.assertEqual(ly.year, 2009, f'The workyear before {now} should be 2009 - 2010')

    def test_logo_save_path(self):
        # Build
        werkjaar = Werkjaar(year=self.some_year)
        raw_filename = 'img44836_s_upload.jpg'  # random string as example

        # Operate
        logo_path = get_yeartheme_logo_path(werkjaar, raw_filename)

        # Check
        self.assertEqual(logo_path, 'img/jaarthema/logo_jaarthema_2010-2009.jpg')

    def test_next_year(self):
        # Build
        some_year = Werkjaar.objects.get(year=self.some_year)

        # Operate
        next_year = some_year.next_year().year

        # Check
        self.assertEqual(next_year, self.some_year + 1,
                         f'The year after {self.some_year} should be {self.some_year + 1}')

    def test_previous_year(self):
        # Build
        some_year = Werkjaar.objects.get(year=self.some_year)

        # Operate
        previous_year = some_year.previous_year().year

        # Check
        self.assertEqual(previous_year, self.some_year - 1,
                         f'The year before {self.some_year} should be {self.some_year - 1}')

    def test_creation_of_new_year_when_calling_next_year(self):
        # Build
        total_years = Werkjaar.objects.count()
        first_year = Werkjaar.objects.get(year=self.last_year)

        # Operate
        first_year.next_year()
        new_total_years = Werkjaar.objects.count()

        # Check
        self.assertEqual(new_total_years, total_years + 1,
                         'A new werkjaar should have been created')

    def test_creation_of_new_year_when_calling_last_year(self):
        # Build
        total_years = Werkjaar.objects.count()
        first_year = Werkjaar.objects.get(year=self.first_year)

        # Operate
        first_year.previous_year()
        new_total_years = Werkjaar.objects.count()

        # Check
        self.assertEqual(new_total_years, total_years + 1,
                         'A new werkjaar should have been created')

    def test_next_year_on_current_year(self):
        # Build
        current_year = Werkjaar.objects.current_year()
        total_years = Werkjaar.objects.count()

        # Operate
        next_year = current_year.next_year()

        # Check
        self.assertIsNone(next_year, 'When calling "next_year()" on the actual current werkjaar, it should return None')
        self.assertEqual(Werkjaar.objects.count(), total_years,
                         'When calling "next_year()" on the actual current werkjaar, '
                         'it should not have created a new werkjaar')
