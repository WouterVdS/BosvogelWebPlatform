from django.http.response import HttpResponse
from django.shortcuts import render

from apps.profile.queries import get_leader_profiles


def index(request, year=None):
    # todo ook voor andere werkjaren een overzicht kunnen zien --> wat met leidingsprofielen? Toch geen profielen van leiding van 20j terug laten zien?

    leaders = get_leader_profiles(year)
    context = {
        'title_suffix': ' - Leiding',
        'leaders': leaders

    }
    return render(request, 'profile/index.html', context)


def profile(request, name):
    # todo profielpagina per leiding met alle gegevens van dien
    # todo leiding niet gevonden weergeven en loggen
    full_name = name # todo de juiste
    context = {
        'title_suffix': f' - {full_name}',
    }
    return render(request, 'profile/profile.html', context)
