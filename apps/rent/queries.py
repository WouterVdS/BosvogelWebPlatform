import logging

from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from apps.rent.models import Pricing

logger = logging.getLogger(__name__)


def get_prices():
    try:
        prices = Pricing.objects.latest('pricesSetOn')
    except ObjectDoesNotExist:
        prices = Pricing(perPersonPerDay=0, dailyMinimum=0, electricitykWh=0, waterSqM=0, gasPerDay=0, deposit=0)
        logger.error('No rent prices set! Go to ' + reverse('rent:manage_rentals') + ' and set pricing for rent!')
    return prices