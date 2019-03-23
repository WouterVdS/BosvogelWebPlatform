from django.contrib import admin

from apps.rent.models import Reservation, Pricing


@admin.register(Reservation)
class RentReservationAdmin(admin.ModelAdmin):  # pragma: no cover
    list_display = ['__str__', 'groupName', 'period', 'contract', 'status', 'depositStatus', 'depositAmount']


@admin.register(Pricing)
class RentPricesAdmin(admin.ModelAdmin):  # pragma: no cover
    list_display = ['perPersonPerDay', 'dailyMinimum', 'electricitykWh', 'waterSqM', 'gasPerDay', 'pricesSetOn']
