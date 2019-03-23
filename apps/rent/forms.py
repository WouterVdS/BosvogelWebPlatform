import datetime

from django import forms

from apps.rent.models import Reservation, Pricing, get_prices


class ReservationForm(forms.ModelForm):  # todo test form!

    startDate = forms.DateField(widget=forms.SelectDateWidget,
                                label='Huren van')
    endDate = forms.DateField(widget=forms.SelectDateWidget,
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

    def clean_period(self):  # todo dit fatsoenlijk uitwerken
        data = self.cleaned_data['period']

        if data.startDate < datetime.date.today():
            raise forms.ValidationError('Das int verleden!')

        return data


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

    def clean(self):  # todo test
        new_prices = super().clean()
        current_prices = get_prices()
        if current_prices.perPersonPerDay == new_prices['perPersonPerDay'] and current_prices.dailyMinimum == \
                new_prices['dailyMinimum'] and current_prices.electricitykWh == new_prices[
            'electricitykWh'] and current_prices.waterSqM == new_prices['waterSqM'] and current_prices.gasPerDay == \
                new_prices['gasPerDay'] and current_prices.deposit == new_prices['deposit']:
            raise forms.ValidationError('Geen verschil met de vorige tarieven.')
