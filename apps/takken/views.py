from django.shortcuts import render, redirect
from django.urls import reverse

from apps.agenda.queries import get_vergaderingen
from apps.home.constants import Takken
from apps.profile.queries import get_active_leader_memberships


def index(request):
    return render(request, 'takken/index.html', {'title_suffix': ' - Takken'})


def tak_overview(request, tak):
    # todo refactor this part
    found = False
    takinfos = [Takken.TAKINFO_KAP, Takken.TAKINFO_WEL, Takken.TAKINFO_KAB, Takken.TAKINFO_JV, Takken.TAKINFO_JG,
                Takken.TAKINFO_V, Takken.TAKINFO_G, Takken.TAKINFO_JIN, Takken.TAKINFO_L, Takken.TAKINFO_GRL]
    found_takinfo = None
    for takinfo in takinfos:
        if takinfo['fullName'].lower() == tak.lower():
            found = True
            found_takinfo = takinfo
            break
    if not found:
        return redirect(reverse('takken:index'))

    memberships = get_active_leader_memberships(found_takinfo['abbrev'])

    vergaderingen = get_vergaderingen(found_takinfo['abbrev'])

    context = {'title_suffix': ' -  ' + found_takinfo['fullName'],
               'tak': found_takinfo['fullName'],
               'takabbreviation': found_takinfo['abbrev'],
               'taklogo': found_takinfo['takteken'],
               'age': found_takinfo['age'],
               'description': found_takinfo['description'],
               'memberships': memberships,
               'vergaderingen': vergaderingen}

    if 'takmail' in found_takinfo:
        context['takmail'] = found_takinfo['takmail']

    return render(request, 'takken/takview.html', context)


def afterleader(request):
    return render(request, 'takken/takken_afterleader.html', {'title_suffix': ' -  Wat na leiding?',
                                                              'tak': 'Wat na leiding?'})
