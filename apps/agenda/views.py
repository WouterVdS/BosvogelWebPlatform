from django.shortcuts import render


def index(request):
    return render(request, 'agenda/agenda.html', {'title_suffix': ' - Agenda'})
