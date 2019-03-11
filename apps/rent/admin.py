from django.contrib import admin

from apps.rent.models import RentReservation


@admin.register(RentReservation)
class RentReservationAdmin(admin.ModelAdmin):  # pragma: no cover
    list_display = ['__str__', 'groupName', 'period', 'contract', 'status', 'depositStatus', 'depositAmount']
