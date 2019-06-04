from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.home.models import Werkjaar
from apps.home.validators import validate_iban_format, validate_international_phone_number

MALE = 'M'
FEMALE = 'V'
SEXES = (
    (MALE, 'Man'),
    (FEMALE, 'Vrouw'),
)


class ProfileManager(models.Manager):
    pass


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    email = models.EmailField(unique=True)
    birthday = models.DateField()
    sex = models.CharField(max_length=2, choices=SEXES)
    phoneNr = models.CharField(max_length=13, validators=[validate_international_phone_number])
    bank_account_number = models.CharField(max_length=19, validators=[validate_iban_format])
    active = models.BooleanField()

    # totem = models.TextField() todo
    # picture = models. todo
    # link to user todo

    def __str__(self):
        fields = []
        if self.first_name:
            fields.append(self.first_name)
        if self.nickname:
            fields.append(f'\'{self.nickname}\'')
        if self.last_name:
            fields.append(self.last_name)
        return ' '.join(fields)


class MembershipManager(models.Manager):
    pass


class Membership(models.Manager):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # todo test
    werkjaar = models.ForeignKey(Werkjaar, on_delete=models.CASCADE)  # todo test

    class Meta:
        unique_together = ['profile', 'werkjaar']  # todo test
