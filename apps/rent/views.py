from django.conf import settings
from django.shortcuts import render, redirect
from rules.contrib.views import permission_required

from apps.rent.forms import ReservationForm, PricingForm
from apps.rent.models import get_prices


def index(request):
    return render(request, 'rent/rent_home.html', {'title_suffix': ' - Verhuur'})


@permission_required('rent.access_rent_management')  # todo test access
def manage_rentals(request):
    return render(request, 'rent/manage_rentals.html', {'title_suffix': ' - Beheer'})


def photos(request):
    return render(request, 'rent/photos.html', {'title_suffix': ' - Verhuur Foto\'s'})


def building_and_terrain(request):
    return render(request, 'rent/building_and_terrain.html', {'title_suffix': ' - Gebouw & Terrein'})


def pricing(request):
    return render(request, 'rent/pricing.html', {'title_suffix': ' - Tarieven',
                                                 'price': get_prices()})


@permission_required('rent.change_pricing')  # todo test access
def change_pricing(request):
    if request.method == 'POST':
        form = PricingForm(request.POST)
        if form.is_valid():  # todo niet opslaan als er niks aangepast is, wel melding van geven
            form.save()
            return redirect('rent:pricing')
        # todo mail groepsleiding and verhuurresponsible when prices changed (and who changed them)
    else:
        form = PricingForm(instance=get_prices())
    return render(request, 'rent/change_pricing.html', {'title_suffix': ' - Verhuur', 'form': form})


def contracts(request):
    return render(request, 'rent/contracts.html', {'title_suffix': ' - Verhuurcontract'})


def reserve(request):  # todo test redirection to check_reservation
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():  # todo eigen checks toevoegen op oa data
            reservation = form.save(commit=False)
            reservation.pricing = get_prices()
            reservation.save()
            form.save_m2m()
            return render(request, 'rent/rent_home.html',
                          {'title_suffix': ' - Verhuur'})  # todo redirect to check reservation or something similar
    else:
        if settings.DEBUG:  # todo remove after finishing development
            form = ReservationForm(initial={
                'groupName': 'Testgroup',
                'town': 'TestTown',
                'email': 'test@test.text',
                'phoneNr': '0471589589',
                'bankAccountNumber': 'BE24 2222 2222 2222',
                'numberOfPeople': '50',
                'comments': 'Hey how hey! test test test test',
            })
        else:
            form = ReservationForm()
    return render(request, 'rent/reserve.html', {'title_suffix': ' - Reserveren', 'form': form})


def check_reservation(request):
    return render(request, 'rent/check_reservation.html', {'title_suffix': ' - Reservatie'})
