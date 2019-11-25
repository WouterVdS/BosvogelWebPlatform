from django.db import models

from apps.home.constants import Takken
from apps.home.models import Werkjaar, get_workyear
from apps.profile.models.profile import Profile


class CurrentYearMembershipManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(werkjaar__year=get_workyear())


class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    werkjaar = models.ForeignKey(Werkjaar, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)
    tak = models.CharField(max_length=3, choices=Takken.TAKKEN, null=True, blank=True)
    tak_leader_name = models.CharField(max_length=32, null=True, blank=True)

    objects = models.Manager()
    current_year = CurrentYearMembershipManager()

    class Meta:
        unique_together = ['profile', 'werkjaar']

    def __str__(self):
        result = f'{self.werkjaar}: {self.profile}'
        if self.tak_leader_name:
            result += f' aka {self.tak_leader_name}'
        if self.is_leader:
            result += ' (leiding)'
        if self.tak:
            result += f' - {self.get_tak_display()}'
        return result
