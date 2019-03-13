from django.shortcuts import render


def index(request):
    return render(request, 'rent/rent_home.html', {'title_suffix': ' - Verhuur'})


def manage_rentals(request):  # todo restrict access with rules
    return render(request, 'rent/manage_rentals.html', {'title_suffix': ' - Beheer\'s'})


def photos(request):
    return render(request, 'rent/photos.html', {'title_suffix': ' - Verhuur Foto\'s'})


def pricing(request):
    return render(request, 'rent/pricing.html', {'title_suffix': ' - Verhuur Tarieven'})


def contracts(request):
    return render(request, 'rent/contracts.html', {'title_suffix': ' - Verhuur Contracten'})


def reserve(request):
    return render(request, 'rent/reserve.html', {'title_suffix': ' - Verhuur Reserveren'})


def check_reservation(request):
    return render(request, 'rent/check_reservation.html', {'title_suffix': ' - Verhuur Reservatie'})
