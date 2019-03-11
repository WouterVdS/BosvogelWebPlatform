from django.db import models

from apps.agenda.models import Event
from apps.place.models import Place

NEW_REQUEST = 'NR'
COMMUNICATING = 'CO'
AWAITING_DEPOSIT = 'AD'
APPROVED = 'AP'
HAPPENING_NOW = 'HN'  # todo check on period and current date + auto set this field
AWAITING_PAYMENT = 'AP'
CANCELLED = 'CA'
DONE = 'DO'

RESERVATION_STATUSES = (
    (NEW_REQUEST, 'Nieuwe aanvraag'),
    (COMMUNICATING, 'Communicatie gestart'),
    (AWAITING_DEPOSIT, 'Wachten op storting voorschot'),
    (APPROVED, 'Goedgekeurd'),
    (HAPPENING_NOW, 'Verhuurperiode nu bezig'),
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
    email = models.EmailField()
    phoneNr = models.CharField(max_length=13)  # todo checks
    period = models.ForeignKey(to=Event, on_delete=models.CASCADE)
    bankAccountNumber = models.CharField(max_length=16)  # todo more checks (use IBAN checksum)
    contract = models.FileField(null=True, blank=True)  # todo pick destination
    status = models.CharField(max_length=3, choices=RESERVATION_STATUSES, default=NEW_REQUEST)
    depositStatus = models.CharField(max_length=1, choices=DEPOSIT_STATUSES, default=AWAITING)
    depositAmount = models.IntegerField(null=True, blank=True)
    finalBill = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)

    def __str__(self):
        return self.groupName + ' ' + str(self.period)

    class Meta:
        verbose_name = 'Reservatie'
        verbose_name_plural = 'Reservaties'
