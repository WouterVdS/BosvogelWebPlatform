from django.shortcuts import render, redirect
from django.urls import reverse

from apps.home.constants import Takken


def index(request):
    return render(request, 'takken/index.html', {'title_suffix': ' - Takken'})


def takview(request, tak):
    # todo refactor this part
    found = False
    for (s, t) in Takken.TAKKEN:
        if t.lower() == tak.lower():
            tak = s
            found = True
            break
    if not found:
        return redirect(reverse('takken:index'))
    return render(request, 'takken/takview.html', {'title_suffix': ' -  ' + t,
                                                   'tak': t})


def afterleaderview(request):
    print("smiljmilj")
    return render(request, 'takken/takview.html', {'title_suffix': ' -  Wat na leiding?',
                                                   'tak': 'Wat na leiding?'})
