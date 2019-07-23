from django.db import models

from apps.home.constants import Takken
from apps.home.models import Werkjaar
from apps.profile.models.profile import Profile


class LeaderManager(models.Manager):

    def get_queryset(self):  # todo test
        return super().get_queryset().filter(is_leader=True)

    @staticmethod
    def get_leaders_for_tak(self, tak):  # todo test
        return Membership.leaders.filter(tak=tak).values()  # todo moet profiles teruggeven


class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    werkjaar = models.ForeignKey(Werkjaar, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)
    tak = models.CharField(max_length=3, choices=Takken.TAKKEN, null=True, blank=True)  # todo test
    is_groupleader = models.BooleanField(
        default=False)  # todo make required Is_leader must be true if is_groupleader is true

    objects = models.Manager()
    leaders = LeaderManager()  # todo test

    class Meta:
        unique_together = ['profile', 'werkjaar']
