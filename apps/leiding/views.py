from django.shortcuts import render


def index(request, year=None):
    context = {
        'title_suffix': ' - Leiding'
    }
    return render(request, 'profile/index.html', context)
