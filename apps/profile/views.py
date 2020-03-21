from django.shortcuts import render

def index(request, year=None):
    # todo ook voor andere werkjaren een overzicht kunnen zien --> wat met leidingsprofielen? Toch geen profielen van leiding van 20j terug laten zien?
    # todo dit hoort hier niet meer, enkel echt voor profielen
    return render(request, 'profile/index.html')


def profile(request, name):
    # todo profielpagina per leiding met alle gegevens van dien
    # todo leiding niet gevonden weergeven en loggen
    full_name = name # todo de juiste
    # todo test
    context = {
        'title_suffix': f' - {full_name}',
    }
    return render(request, 'profile/profile.html', context)
