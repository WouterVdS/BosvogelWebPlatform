from django.core.management.base import BaseCommand

from apps.agenda.models import dangling_rental_event_count
from apps.profile.models.totem import dangling_totem_count


class Command(BaseCommand):
    help = 'Checks if there are objects which have lost their parent and can be deleted'

    def handle(self, *args, **kwargs):
        print('\n')

        print('As a result of bulk creating/editing/deleting of objects, '
              'signals are not propagated. This can result in unwanted behavior.'
              'If all is good, this list should only contain zero\'s:')
        results = [
            ['dangling totems', dangling_totem_count(),
             'totem(s) found of which the profile is deleted'],
            ['dangling rental events', dangling_rental_event_count(),
             'rental event(s) found of which the reservation is deleted']
        ]

        for result in results:
            print(f'\t{result[0]}:\t{result[1]}', end='')
            if result[1] != 0:
                print(f' {result[2]}', end='')
            print('')
