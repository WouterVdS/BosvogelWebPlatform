from django.shortcuts import render

from apps.home.constants import Takken
from apps.profile.queries import get_leader_memberships


def index(request, year=None):
    takken = []
    all_leaders = list(get_leader_memberships(year))
    for abbrev, tak in Takken.TAKKEN:
        if abbrev is Takken.LEIDING:
            continue
        leiding = [leider for leider in all_leaders if leider.tak == abbrev]
        takken.append([tak, leiding])

    context = {
        'title_suffix': ' - Leiding',
        'takken': takken
    }
    return render(request, 'leiding/index.html', context)
