from django.db import models
from django.dispatch import receiver

from apps.agenda.models import Event
from apps.place.models import Place
from apps.rent.validators import validate_international_phone_number, validate_iban_format

NEW_REQUEST = 'NR'
COMMUNICATING = 'CO'
AWAITING_CONTRACT = 'AC'
AWAITING_DEPOSIT = 'AD'
APPROVED = 'AP'
AWAITING_PAYMENT = 'AP'
CANCELLED = 'CA'
DONE = 'DO'

RESERVATION_STATUSES = (
    (NEW_REQUEST, 'Nieuwe aanvraag'),
    (COMMUNICATING, 'Communicatie gestart'),
    (AWAITING_CONTRACT, 'Wachten op contract'),
    (AWAITING_DEPOSIT, 'Wachten op storting voorschot'),
    (APPROVED, 'Goedgekeurd'),
    (AWAITING_PAYMENT, 'Afwachten betaling eindafrekening'),
    (CANCELLED, 'Afgezegd'),
    (DONE, 'Afgelopen'),
)

AWAITING = 'A'
DEPOSITED = 'D'
REFUNDED = 'R'

DEPOSIT_STATUSES = (
    (AWAITING, 'In afwachting'),
    (DEPOSITED, 'Gestort'),
    (REFUNDED, 'Terugbetaald')
)


class RentReservation(models.Model):
    groupName = models.CharField(max_length=64)
    town = models.CharField(max_length=32)
    email = models.EmailField()
    phoneNr = models.CharField(max_length=13, validators=[validate_international_phone_number])
    period = models.ForeignKey(null=True, to=Event, on_delete=models.SET_NULL)
    bankAccountNumber = models.CharField(max_length=19, validators=[validate_iban_format])
    contract = models.FileField(null=True, blank=True)  # todo pick destination
    status = models.CharField(max_length=3, choices=RESERVATION_STATUSES, default=NEW_REQUEST)
    depositStatus = models.CharField(max_length=1, choices=DEPOSIT_STATUSES, default=AWAITING)
    depositAmount = models.IntegerField(null=True, blank=True)
    numberOfPeople = models.IntegerField()
    checklist = models.TextField(null=True, blank=True)  # todo convert to json?
    finalBill = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Reservatie'
        verbose_name_plural = 'Reservaties'

    def __str__(self):
        return self.groupName + ' (' + self.town + '), ' + str(self.period.startDate) + ' - ' + str(self.period.endDate)


@receiver(models.signals.post_delete, sender=RentReservation)
def handle_deleted_profile(sender, instance, **kwargs):
    if instance.period:
        instance.period.delete()
