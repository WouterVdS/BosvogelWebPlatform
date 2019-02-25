from django.contrib import admin

from apps.place.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'zipcode', 'city', 'street_and_number', 'latitude', 'longitude']
    list_filter = ['country', 'city']
