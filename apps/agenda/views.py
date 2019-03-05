from django.shortcuts import render


def agenda(request):
    return render(request, 'agenda/agenda.html', {'title_suffix': ' - Agenda'})  # todo add 'Den Bosvogel' view
