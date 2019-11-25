from django.db import models

from apps.home.constants import Takken, Events
from apps.place.models import Place


def dangling_rental_event_count():
    return Event.rentals.filter(reservation=None).count()


class RentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=Events.RENTAL)

    def new_rental(self, start_date, end_date, event_name):
        return self.create(
            name=event_name,
            startDate=start_date,
            endDate=end_date,
            startTime=Events.DEFAULT_RENT_START_TIME,
            endTime=Events.DEFAULT_RENT_ENDING_TIME,
            type=Events.RENTAL
        )

    def is_available_for_rent(self, start_date, end_date):
        if self.get_queryset().filter(startDate__exact=start_date, endDate__exact=end_date):
            return False
        elif self.get_queryset().filter(startDate__lte=start_date, endDate__gt=end_date).exists():
            return False
        elif self.get_queryset().filter(startDate__gt=start_date, endDate__lt=end_date).exists():
            return False
        elif self.get_queryset().filter(startDate__gt=start_date, startDate__lt=end_date).exists():
            return False
        elif self.get_queryset().filter(endDate__gt=start_date, endDate__lte=end_date).exists():
            return False
        return True


class Event(models.Model):
    name = models.CharField(max_length=64, null=True, blank=True)
    place = models.ForeignKey(to=Place, null=True, blank=True, on_delete=models.SET_NULL)
    startDate = models.DateField()
    endDate = models.DateField(null=True, blank=True)
    startTime = models.TimeField(null=True, blank=True)
    endTime = models.TimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=4, choices=Events.EVENT_TYPES)
    tak = models.CharField(max_length=3, null=True, blank=True, choices=Takken.TAKKEN)

    objects = models.Manager()
    rentals = RentManager()

    class Meta:
        ordering = ['startDate', 'startTime']

    def save(self, *args, **kwargs):
        if not self.endDate:
            self.endDate = self.startDate
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        fields = []
        if self.name:
            fields.append(str(self.name))
        if self.place:
            fields.append(str(self.place))
        if self.startDate:
            fields.append(str(self.startDate))
        if self.endDate:
            fields.append(str(self.endDate))
        if self.startTime:
            fields.append(str(self.startTime))
        if self.endTime:
            fields.append(str(self.endTime))
        if self.description:
            fields.append(self.description)
        if self.type:
            fields.append(str(self.get_type_display()))
        if self.tak:
            fields.append(str(self.get_tak_display()))
        return ', '.join(fields)
