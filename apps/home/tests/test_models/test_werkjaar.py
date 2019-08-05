from django.test import TestCase

from apps.home.models import Werkjaar, get_yeartheme_logo_path


class WerkjaarTestCase(TestCase):

    first_year = 2000
    some_year = 2010
    last_year = 2020

    def setUp(self):
        for x in range(self.first_year, self.last_year + 1):
            Werkjaar.objects.create(year=x)

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

    def test_calling_next_year_when_it_does_not_exist_creates_a_log(self):
        with self.assertLogs(level='WARNING') as loggerWatcher:
            # Build
            last = Werkjaar.objects.get(year=self.last_year)

            # Operate
            last.next_year()

            # Check
            self.assertIn('A new werkjaar object was created for werkjaar',
                          loggerWatcher.output[0],
                          'It should log the warning that a new werkjaar is created')

    def test_calling_previous_year_when_it_does_not_exist_creates_a_log(self):
        with self.assertLogs(level='WARNING') as loggerWatcher:
            # Build
            first = Werkjaar.objects.get(year=self.first_year)

            # Operate
            first.previous_year()

            # Check
            self.assertIn('A new werkjaar object was created for werkjaar',
                          loggerWatcher.output[0],
                          'It should log the warning that a new werkjaar is created')
