from django.db import models


class Totem(models.Model):
    kleurentotem = models.CharField(null=True, blank=True, max_length=64)
    kleurentotem_text = models.TextField(null=True, blank=True)
    voortotem = models.CharField(null=True, blank=True, max_length=64)
    voortotem_text = models.TextField(null=True, blank=True)
    totem = models.CharField(null=True, blank=True, max_length=64)
    totem_text = models.TextField(null=True, blank=True)

    def __str__(self):
        fields = []
        if self.kleurentotem:
            fields.append(self.kleurentotem)
        if self.voortotem:
            fields.append(self.voortotem)
        if self.totem:
            fields.append(self.totem)
        return ' '.join(fields)

    def save(self, *args, **kwargs):
        if self.kleurentotem:
            self.kleurentotem = self.kleurentotem.lower()
        if self.voortotem:
            self.voortotem = self.voortotem.lower()
        if self.totem:
            self.totem = self.totem.lower()
        return super(Totem, self).save(*args, **kwargs)
