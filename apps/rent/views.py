from django.shortcuts import render, redirect
from rules.contrib.views import permission_required

from apps.agenda.models import Event
from apps.rent.forms import ReservationForm, PricingForm
from apps.rent.models import get_prices, Reservation


def index(request):
    return render(request, 'rent/rent_home.html', {'title_suffix': ' - Verhuur'})


@permission_required('rent.access_rent_management')  # todo test access
def manage_rentals(request):  # todo test  perofrmance objects.select_related()
    return render(request, 'rent/manage_rentals.html', {'title_suffix': ' - Beheer',
                                                        'rentals': Reservation.objects.all()})


def photos(request):
    return render(request, 'rent/photos.html', {'title_suffix': ' - Verhuur Foto\'s'})


def building_and_terrain(request):
    return render(request, 'rent/building_and_terrain.html', {'title_suffix': ' - Gebouw & Terrein'})


def pricing(request):
    return render(request, 'rent/pricing.html', {'title_suffix': ' - Tarieven',
                                                 'price': get_prices()})


@permission_required('rent.change_pricing')
def change_pricing(request):
    if request.method == 'POST':
        form = PricingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rent:pricing')
        # todo mail groepsleiding and verhuurresponsible when prices changed (and who changed them)
    else:
        form = PricingForm(instance=get_prices())
    return render(request, 'rent/change_pricing.html', {'title_suffix': ' - Verhuur', 'form': form})


def contracts(request):
    return render(request, 'rent/contracts.html', {'title_suffix': ' - Verhuurcontract'})


# todo verhuur
"""
    transacties apart bijhouden
    op basis van de transacties (onsave) de status aanpassen
    nakijken van bedrag betaald etc.
    Dit volledig uischrijven en op issue zetten
    event sourced maken van de te betalen/betalen bedragen
    workflow uittekenen (en bij admins laten zien?)
"""


def reserve(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data

            rentEvent = Event.rentals.new_rental(
                formData['startDate'],
                formData['endDate'],
                'Verhuur - ' + formData['groupName'])

            reservation = form.save(commit=False)
            reservation.pricing = get_prices()
            reservation.period = rentEvent
            reservation.save()

            return redirect('rent:index')  # todo redirect to check reservation or something similar
    else:
        form = ReservationForm()
    return render(request, 'rent/reserve.html', {'title_suffix': ' - Reserveren', 'form': form})


def check_reservation(request):
    return render(request, 'rent/check_reservation.html', {'title_suffix': ' - Reservatie'})
