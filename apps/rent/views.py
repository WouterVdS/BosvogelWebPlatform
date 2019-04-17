from django.contrib import messages
from django.core import mail
from django.shortcuts import render, redirect
from django.urls import reverse
from rules.contrib.views import permission_required

from BosvogelWebPlatform import settings
from BosvogelWebPlatform.settings import EMAIL_ADDRESS_RENT, EMAIL_ADDRESS_NOREPLY
from apps.agenda.models import Event
from apps.rent.forms import ReservationForm, PricingForm
from apps.rent.models import get_prices, Reservation, Pricing


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
    current_prices = get_prices()
    if current_prices.perPersonPerDay is 0:
        mail.send_mail('ERROR - Verhuur prijzen zijn nog niet gezet!',  # todo better test this mail
                       'Iemand probeerde het lokaal te huren, \n'
                       + 'maar zolang er geen verhuurpijzen ingesteld zijn is het onmogelijk om reservaties te maken.\n'
                       + 'Surf zo snel mogelijk naar onderstaande link om de verhuurtarieven in te stellen:\n'
                       + request.build_absolute_uri(reverse('rent:change_pricing')),
                       from_email=EMAIL_ADDRESS_NOREPLY,
                       recipient_list=[EMAIL_ADDRESS_RENT])  # todo add group leaders
    return render(request, 'rent/pricing.html', {'title_suffix': ' - Tarieven',
                                                 'price': current_prices})


@permission_required('rent.change_pricing')
def change_pricing(request):
    if request.method == 'POST':
        form = PricingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Verhuurtarieven aangepast')
            new_prices = Pricing.objects.order_by('-pricesSetOn')[0]
            if Pricing.objects.count() > 1:
                prev = Pricing.objects.order_by('-pricesSetOn')[1]
            else:
                prev = Pricing(
                    perPersonPerDay=0,
                    dailyMinimum=0,
                    electricitykWh=0,
                    waterSqM=0,
                    gasPerDay=0,
                    deposit=0)
            mail.send_mail('Opgelet, de verhuurpijzen zijn aangepast.',
                           f'De verhuurtarieven zijn aangepast door {request.user}. De nieuwe prijzen zijn :\n'
                           + f'Per persoon per dag: \t€ {prev.perPersonPerDay} --> € {new_prices.perPersonPerDay}\n'
                           + f'Dagelijks minimum \t\t€ {prev.dailyMinimum} --> € {new_prices.dailyMinimum}\n'
                           + f'Electriciteit per kWh: \t€ {prev.electricitykWh} --> € {new_prices.electricitykWh}\n'
                           + f'Water per m³: \t\t\t€ {prev.waterSqM} --> € {new_prices.waterSqM}\n'
                           + f'Gas per dag: \t\t\t€ {prev.gasPerDay} --> € {new_prices.gasPerDay}\n'
                           + f'Waarborg: \t\t\t\t€ {prev.deposit} --> € {new_prices.deposit}\n'
                           + 'Surf naar '
                           + request.build_absolute_uri(reverse('rent:change_pricing'))
                           + ' om ze aan te passen als dit een fout was.',
                           from_email=EMAIL_ADDRESS_NOREPLY,  # todo better test this mail
                           recipient_list=[EMAIL_ADDRESS_RENT])  # todo when user app finished send to grl
            return redirect('rent:pricing')
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
        if not Pricing.objects.all().exists():
            messages.warning(request, 'Reserveren tijdelijk niet mogelijk.')
            # todo use the same template as in the pricing view
            mail.send_mail(f'ERROR - Verhuur prijzen zijn nog niet gezet!',
                           'Iemand probeerde het lokaal te huren, \n'
                           + 'maar zolang er geen verhuurpijzen ingesteld zijn is het onmogelijk om reservaties te maken.\n'
                           + 'Surf zo snel mogelijk naar onderstaande link om de verhuurtarieven in te stellen:\n'
                           + request.build_absolute_uri(reverse('rent:change_pricing')),
                           EMAIL_ADDRESS_NOREPLY,
                           [EMAIL_ADDRESS_RENT])  # todo add grl
            return redirect('rent:index')
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

            messages.success(request, 'Reservatie gelukt! Check je mailbox voor meer informatie.')
            # todo richer email body through template
            # todo add contract as attachment
            mail.send_mail(f'Scouts Bosvogels - Verhuur {reservation.groupName}, '
                           f'{reservation.period.startDate} - {reservation.period.endDate}',
                           'Nieuwe reservatie',
                           EMAIL_ADDRESS_RENT,
                           [reservation.email])
            # todo richer email body through template
            mail.send_mail(f'Nieuwe verhuuraanvraag - {reservation.groupName}, '
                           f'{reservation.period.startDate} - {reservation.period.endDate}',
                           'Nieuwe verhuuraanvraag',
                           EMAIL_ADDRESS_NOREPLY,
                           [EMAIL_ADDRESS_RENT])

            return redirect('rent:reserve')
    else:
        if settings.DEBUG:  # todo remove after finishing development
            if Event.rentals.all().exists():
                end = Event.rentals.latest('endDate').endDate
                form = ReservationForm(initial={
                    'groupName': 'Testgroup',
                    'town': 'TestTown',
                    'email': 'test@test.text',
                    'phoneNr': '0471589589',
                    'bankAccountNumber': 'BE24 2222 2222 2222',
                    'numberOfPeople': '50',
                    'comments': 'Hey how hey! test test test test',
                    'startDate': f'{end.day}-{end.month}-{end.year}',
                    'endDate': f'{end.day + 1}-{end.month}-{end.year}'
                })
            else:
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
