import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from apps.agenda.models import Event
from apps.home.validators import validate_phone_number, validate_iban_format
from apps.place.models import Place

logger = logging.getLogger(__name__)

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


class Pricing(models.Model):
    perPersonPerDay = models.DecimalField(max_digits=5, decimal_places=2)
    dailyMinimum = models.DecimalField(max_digits=5, decimal_places=2)
    electricitykWh = models.DecimalField(max_digits=5, decimal_places=2)
    waterSqM = models.DecimalField(max_digits=5, decimal_places=2)
    gasPerDay = models.DecimalField(max_digits=5, decimal_places=2)
    deposit = models.DecimalField(max_digits=5, decimal_places=2)
    pricesSetOn = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tarieven'
        verbose_name_plural = 'Tarieven'

    def __str__(self):
        return 'Pricing (' + str(self.pricesSetOn) + ')'


class Reservation(models.Model):
    # todo add depositDeadline, add this in email, overviews, admin, crontab to send mails, ....
    groupName = models.CharField(max_length=64)
    town = models.CharField(max_length=32)
    email = models.EmailField()
    phoneNr = models.CharField(max_length=13, validators=[validate_phone_number])
    period = models.ForeignKey(null=True, to=Event, on_delete=models.SET_NULL)
    pricing = models.ForeignKey(null=True, to=Pricing, on_delete=models.SET_NULL)
    bankAccountNumber = models.CharField(max_length=19, validators=[validate_iban_format])
    contract = models.FileField(null=True, blank=True)  # todo pick destination
    status = models.CharField(max_length=3, choices=RESERVATION_STATUSES, default=NEW_REQUEST)
    depositStatus = models.CharField(max_length=1, choices=DEPOSIT_STATUSES, default=AWAITING)
    depositAmount = models.IntegerField(null=True, blank=True)
    numberOfPeople = models.IntegerField()
    checklist = models.TextField(null=True, blank=True)  # todo convert to jsonb?
    finalBill = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=2)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Reservatie'
        verbose_name_plural = 'Reservaties'

    def __str__(self):
        if self.period:
            return self.groupName + ' (' + self.town + '), ' + str(self.period.startDate) + ' - ' + str(
                self.period.endDate)
        return self.groupName + ' (' + self.town + ')'


# todo managment functie maken die checkt of er periods zijn waar geen reservation meer aanhangt
# dit zou niet mogen, maar signals worden soms overgeslagen (bij bulk operaties)
# let op dat type van period wel rent moet zijn
# test schrijven die bulk delete doet
@receiver(models.signals.post_delete, sender=Reservation)
def handle_deleted_reservation(sender, instance, **kwargs):
    if instance.period:
        instance.period.delete()


def get_prices():
    try:
        prices = Pricing.objects.latest('pricesSetOn')
    except ObjectDoesNotExist:
        prices = Pricing(perPersonPerDay=0, dailyMinimum=0, electricitykWh=0, waterSqM=0, gasPerDay=0, deposit=0)
        logger.error('No rent prices set! Go to ' + reverse('rent:manage_rentals') + ' and set pricing for rent!')
    return prices
