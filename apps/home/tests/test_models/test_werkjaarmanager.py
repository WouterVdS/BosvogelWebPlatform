from datetime import date

from django.test import TestCase

from apps.home.models import Werkjaar


class WerkjaarManagerTestCase(TestCase):

    first_year = 2000
    some_year = 2010
    last_year = 2020

    def setUp(self):
        for x in range(self.first_year, self.last_year + 1):
            Werkjaar.objects.create(year=x)

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

    def test_next_year_on_current_year(self):
        # Build
        current_year = Werkjaar.objects.current_year()

        # Operate
        next_year = current_year.next_year()

        # Check
        self.assertIsNotNone(next_year,
                             'It should return a werkjaar')

    def test_current_year_when_no_werkjaar_exists(self):
        # Operate
        Werkjaar.objects.all().delete()
        current_year = Werkjaar.objects.current_year()

        # Check
        self.assertIsNotNone(current_year,
                             'A new werkjaar should be created')

    def test_if_calling_current_year_when_no_werkjaar_exists_creates_a_log(self):
        with self.assertLogs(level='WARNING') as loggerWatcher:
            # Operate
            Werkjaar.objects.all().delete()
            Werkjaar.objects.current_year()

            # Check
            self.assertIn('which did not exist so a new one is created',
                          loggerWatcher.output[0],
                          'It should log the warning that a new werkjaar is created')

    def test_current_year_for_date(self):
        # Build
        dates = [
            [date(2019, 8, 31), 2018],
            [date(2019, 9, 1), 2019],
            [date(2019, 1, 1), 2018],
            [date(2019, 12, 31), 2019],
        ]

        for test_line in dates:
            # Operate
            result = Werkjaar.objects.current_year(test_line[0]).year

            # Check
            self.assertEqual(result, test_line[1],
                             f'{test_line[0]} should be in workyear {test_line[1] - 1} - {test_line[1]}')
