from django.db import models
from django.dispatch import receiver

from apps.home.constants import Sex
from apps.home.validators import validate_iban_format, validate_phone_number
from apps.profile.models.totem import Totem


class Profile(models.Model):
    first_name = models.CharField(blank=True, null=True, max_length=30)
    last_name = models.CharField(blank=True, null=True, max_length=150)
    nickname = models.CharField(blank=True, null=True, max_length=30)
    email = models.EmailField(blank=True, null=True, unique=True)
    public_email = models.EmailField(blank=True, null=True, unique=True)
    birthday = models.DateField(blank=True, null=True)
    sex = models.CharField(blank=True, null=True, max_length=2, choices=Sex.SEXES)
    totem = models.ForeignKey(Totem, blank=True, null=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=13, blank=True, null=True,
                                    validators=[validate_phone_number])
    bank_account_number = models.CharField(max_length=19, blank=True, null=True,
                                           validators=[validate_iban_format])

    # picture = models. todo

    def __str__(self):
        fields = []
        if self.first_name:
            fields.append(self.first_name)
        if self.nickname:
            fields.append(f'\'{self.nickname}\'')
        if self.last_name:
            fields.append(self.last_name)
        return ' '.join(fields)


@receiver(models.signals.post_delete, sender=Profile)
def handle_deleted_profile(sender, instance, **kwargs):
    if instance.totem:
        instance.totem.delete()
