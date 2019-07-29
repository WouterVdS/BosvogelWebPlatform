from django.db import models

from apps.home.constants import Takken
from apps.home.models import Werkjaar
from apps.profile.models.profile import Profile


class Membership(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    werkjaar = models.ForeignKey(Werkjaar, on_delete=models.CASCADE)
    is_leader = models.BooleanField(default=False)
    tak = models.CharField(max_length=3, choices=Takken.TAKKEN, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        unique_together = ['profile', 'werkjaar']
