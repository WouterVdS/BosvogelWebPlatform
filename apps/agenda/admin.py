from django.contrib import admin

from apps.agenda.models import Event
from apps.home.constants import Events


class EmptyReservationFilter(admin.SimpleListFilter):

    title = 'dangling event due to deleted reservation'
    parameter_name = 'has_reservation'

    def lookups(self, request, model_admin):
        return (
            ('no', 'Is dangling'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'no':
            return queryset.filter(type=Events.RENTAL, reservation=None)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):  # pragma: no cover
    list_display = ['name', 'place', 'startDate', 'startTime', 'endDate', 'endTime', 'description', 'type', 'tak']
    list_filter = ['type', 'tak', EmptyReservationFilter]
