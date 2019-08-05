from django.shortcuts import render

from apps.agenda.queries import get_vergaderingen, get_public_and_jincafe_events


def index(request):
    vergaderingen = get_vergaderingen()
    events = get_public_and_jincafe_events()
    return render(request, 'agenda/index.html', {'title_suffix': ' - Agenda',
                                                 'events': events,
                                                 'vergaderingen': vergaderingen})
