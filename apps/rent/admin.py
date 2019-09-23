from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.rent.models import Reservation, Pricing


@admin.register(Reservation)
class RentReservationAdmin(admin.ModelAdmin):  # pragma: no cover
    @staticmethod
    def pricing_link(reservation):
        url = reverse('admin:rent_pricing_change', args=[reservation.pricing_id])
        link = f'<a href="{url}">{reservation.pricing}</a>'
        return mark_safe(link)

    @staticmethod
    def period_link(reservation):
        url = reverse('admin:agenda_event_change', args=[reservation.period_id])
        link = f'<a href="{url}">{reservation.period}</a>'
        return mark_safe(link)

    list_display = ['__str__', 'groupName', 'numberOfPeople', 'period_link', 'contract',
                    'pricing_link', 'status', 'depositStatus', 'depositAmount']
    list_filter = ['status']


@admin.register(Pricing)
class RentPricesAdmin(admin.ModelAdmin):  # pragma: no cover
    list_display = ['perPersonPerDay', 'dailyMinimum', 'electricitykWh', 'waterSqM', 'gasPerDay', 'pricesSetOn']
