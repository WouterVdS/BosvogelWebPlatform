import logging
from datetime import date

from django.db import models

from utils.model_utils import OverwriteOnSameNameStorage

logger = logging.getLogger(__name__)


def get_yeartheme_logo_path(instance, filename):
    filename_extension = filename.split('.')[-1]
    return f'img/jaarthema/logo_jaarthema_{instance.year}-{instance.year-1}.{filename_extension}'


def get_workyear(now=date.today()):  # todo wouter tests naar hier laten wijzen
    september_first = date(now.year, 9, 1)
    year = now.year
    if now < september_first:
        year -= 1
    return year


class WerkjaarManager(models.Manager):
    def current_year(self, now=date.today()): # todo wouter alles dat dit gebruikt en enkel het jaar nodig heeft de get_workyear laten pakken
        werkjaar, created = self.get_or_create(year=get_workyear(now))
        if created:
            logger.warning(f'Werkjaar.objects.current_year is called for {now},'
                           f' which did not exist so a new one is created')
        return werkjaar

    def last_year(self, now=date.today()):
        return self.current_year(now).previous_year()


class Werkjaar(models.Model):
    year = models.IntegerField(unique=True)
    yearTheme = models.CharField(blank=True, max_length=255)
    yearThemeLogo = models.ImageField(blank=True,
                                      storage=OverwriteOnSameNameStorage(),
                                      upload_to=get_yeartheme_logo_path)
    yearThemeSong = models.URLField(blank=True)

    objects = WerkjaarManager()

    def __str__(self):
        return str(self.year) + " - " + str(self.year + 1)

    class Meta:
        verbose_name_plural = 'Werkjaren'
        ordering = ['-year']

    def next_year(self):
        werkjaar, created = Werkjaar.objects.get_or_create(year=self.year + 1)
        if created:
            logger.warning(f'A new werkjaar object was created for werkjaar {werkjaar.year} - {werkjaar.year + 1} '
                           f'due to calling werkjaar.next_year()')
        return werkjaar

    def previous_year(self):
        werkjaar, created = Werkjaar.objects.get_or_create(year=self.year - 1)
        if created:
            logger.warning(f'A new werkjaar object was created for werkjaar {werkjaar.year} - {werkjaar.year + 1} '
                           f'due to calling werkjaar.previous_year()')
        return werkjaar
