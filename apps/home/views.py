from django.shortcuts import render


def index(request):
    return render(request, 'home/landing.html', {'title_suffix': ' - Home'})
