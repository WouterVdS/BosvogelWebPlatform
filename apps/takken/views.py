from django.shortcuts import render, redirect
from django.urls import reverse

from apps.agenda.queries import get_vergaderingen
from apps.home.constants import Takken
from apps.profile.queries import get_active_leader_memberships


def index(request):
    return render(request, 'takken/index.html', {'title_suffix': ' - Takken'})


def tak(request, tak):
    # todo refactor this part

    found = False
    takinfos = [Takken.TAKINFO_KAP, Takken.TAKINFO_WEL, Takken.TAKINFO_KAB, Takken.TAKINFO_JV, Takken.TAKINFO_JG,
                Takken.TAKINFO_V, Takken.TAKINFO_G, Takken.TAKINFO_JIN, Takken.TAKINFO_L, Takken.TAKINFO_GRL]
    for takinfo in takinfos:
        if takinfo['fullName'].lower() == tak.lower():
            found = True
            break
    if not found:
        return redirect(reverse('takken:index'))

    memberships = get_active_leader_memberships(takinfo['abbrev'])

    vergaderingen = get_vergaderingen(takinfo['abbrev'])

    context = {'title_suffix': ' -  ' + takinfo['fullName'],
               'tak': takinfo['fullName'],
               'takabbreviation': takinfo['abbrev'],
               'taklogo': takinfo['takteken'],
               'age': takinfo['age'],
               'description': takinfo['description'],
               'memberships': memberships,
               'vergaderingen': vergaderingen}

    if 'takmail' in takinfo:
        context['takmail'] = takinfo['takmail']

    return render(request, 'takken/takview.html', context)


def afterleader(request):
    return render(request, 'takken/takview.html', {'title_suffix': ' -  Wat na leiding?',
                                                   'tak': 'Wat na leiding?'})
