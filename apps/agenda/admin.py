# todo register models
from django.contrib import admin

from apps.agenda.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):  # pragma: no cover
    list_display = ['name', 'place', 'startDate', 'startTime', 'endDate', 'endTime', 'description', 'type', 'tak']
    list_filter = ['type', 'tak']
