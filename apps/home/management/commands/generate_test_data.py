from django.core.management.base import BaseCommand

from apps.home.management.commands.MockBuilder import MockBuilder


class Command(BaseCommand):
    help = 'Fills the database with random data, simulating a year of use'

    def add_arguments(self, parser):
        parser.add_argument('-y', '--years', type=int, help='Indicates the number of years to generate data for')

    def handle(self, *args, **kwargs):
        print('\n')

        years = kwargs['years']

        if years is None:
            years = 2

        mock_builder = MockBuilder()
        mock_builder.fill_database_with_objects(years)
