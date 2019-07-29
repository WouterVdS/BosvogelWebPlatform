import logging
from datetime import date

from django.db import models

from utils.model_utils import OverwriteOnSameNameStorage

logger = logging.getLogger(__name__)


def get_yeartheme_logo_path(instance, filename):
    filename_extension = filename.split('.')[-1]
    return f'img/jaarthema/logo_jaarthema_{instance.year}-{instance.year-1}.{filename_extension}'


class WerkjaarManager(models.Manager):
    def current_year(self, now=date.today()):
        september_first = date(now.year, 9, 1)
        if now >= september_first:
            return self.get(year=now.year)
        return self.get(year=now.year - 1)

    def last_year(self, now=date.today()):
        return self.current_year(now).previous_year()


class Werkjaar(models.Model):
    objects = WerkjaarManager()
    year = models.IntegerField(unique=True)
    yearTheme = models.CharField(blank=True, max_length=255)
    yearThemeLogo = models.ImageField(blank=True,
                                      storage=OverwriteOnSameNameStorage(),
                                      upload_to=get_yeartheme_logo_path)
    yearThemeSong = models.URLField(blank=True)

    def __str__(self):
        return str(self.year) + " - " + str(self.year + 1)

    class Meta:
        verbose_name_plural = 'Werkjaren'
        ordering = ['-year']

    def next_year(self):
        if self == Werkjaar.objects.current_year():
            logger.warning(f'werkjaar.next_year() is called on the current year ({self.year}) and thus returned None')
            return None
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
