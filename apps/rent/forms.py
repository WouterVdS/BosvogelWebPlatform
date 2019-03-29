import datetime

from django import forms

from apps.agenda.models import Event
from apps.rent.models import Reservation, Pricing, get_prices


# noinspection PyPep8Naming
class ReservationForm(forms.ModelForm):

    startDate = forms.DateField(widget=forms.SelectDateWidget,
                                required=True,
                                label='Huren van')
    endDate = forms.DateField(widget=forms.SelectDateWidget,
                              required=True,
                              label='Huren tot')

    class Meta:
        model = Reservation
        fields = [
            'groupName',
            'town',
            'email',
            'phoneNr',
            'bankAccountNumber',
            'startDate',
            'endDate',
            'numberOfPeople',
            'comments'
        ]
        labels = {
            'groupName': 'Groepsnaam',
            'town': 'Gemeente',
            'email': 'E-mail',
            'phoneNr': 'GSM nummer',
            'bankAccountNumber': 'Rekeningnummer',
            'numberOfPeople': 'Aantal personen (schatting)',
            'comments': 'Extra commentaar of vragen',
        }
        help_texts = {
            'email': 'Gebruik een zo algemeen mogelijk email adres, vb: info@organisatie.be',
        }

    def clean(self):
        data = super().clean()

        startDate = data['startDate']
        endDate = data['endDate']

        if startDate < datetime.date.today():
            raise forms.ValidationError('Gelieve een datum in de toekomst aan te duiden')
        if startDate.month not in [6, 7, 8, 9]:  # june, july, august, and september
            raise forms.ValidationError('Het is enkel mogelijk om tijdens de zomervakantie te huren')
        if endDate < datetime.date.today():
            raise forms.ValidationError('Gelieve een datum in de toekomst aan te duiden')
        if endDate.month not in [6, 7, 8, 9]:  # june, july, august, and september
            raise forms.ValidationError('Het is enkel mogelijk om tijdens de zomervakantie te huren')

        if startDate > endDate:
            raise forms.ValidationError('De einddatum moet na de startdatum komen')

        if not Event.rentals.is_available_for_rent(startDate, endDate):
            raise forms.ValidationError('Deze periode is niet volledig vrij om te huren')


class PricingForm(forms.ModelForm):
    class Meta:
        model = Pricing
        fields = [
            'perPersonPerDay',
            'dailyMinimum',
            'electricitykWh',
            'waterSqM',
            'gasPerDay',
            'deposit',
        ]
        labels = {
            'perPersonPerDay': 'Per persoon per dag',
            'dailyMinimum': 'Minimum dagelijks bedrag',
            'electricitykWh': 'Electriciteitsprijs per kWh',
            'waterSqM': 'Waterprijs per m³',
            'gasPerDay': 'Gasprijs per dag',
            'deposit': 'Waarborg',
        }
        help_texts = {
            'dailyMinimum': 'Minimale dagprijs berekend op enkel het aantal personen.',
        }

    def clean(self):
        data = super().clean()
        current_prices = get_prices()
        if current_prices.perPersonPerDay == data.get('perPersonPerDay') and current_prices.dailyMinimum == \
                data.get('dailyMinimum') and current_prices.electricitykWh == data.get('electricitykWh') and \
                current_prices.waterSqM == data.get('waterSqM') and current_prices.gasPerDay == \
                data.get('gasPerDay') and current_prices.deposit == data.get('deposit'):
            raise forms.ValidationError('Geen verschil met de vorige tarieven.')
