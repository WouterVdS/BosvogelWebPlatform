from urllib import parse

from django.db import models


class Place(models.Model):
    name = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=64)
    zipcode = models.CharField(blank=True, max_length=8)
    city = models.CharField(blank=True, max_length=64)
    street_and_number = models.CharField(blank=True, max_length=64)
    latitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)
    longitude = models.DecimalField(blank=True, null=True, max_digits=9, decimal_places=6)

    def __str__(self):
        fields = []
        if self.name:
            fields.append(self.name)
        if self.street_and_number:
            fields.append(self.street_and_number)
        if self.zipcode:
            fields.append(self.zipcode)
        if self.city:
            fields.append(self.city)
        if self.latitude and self.longitude:
            fields.append(' lat: ' + str(self.latitude) + ', long: ' + str(self.longitude))
        if self.country:
            if self.country.lower() not in ['belgië', 'belgie', 'belgium']:
                fields.append(self.country)
        return ', '.join(fields)

    def link_to_maps(self):
        search_string = ''
        if self.latitude and self.longitude:
            search_string += str(self.latitude) + ',' + str(self.longitude)
        else:
            if self.street_and_number:
                search_string += self.street_and_number + ', '
            if self.zipcode:
                search_string += self.zipcode + ' '
            if self.city:
                search_string += self.city
            search_string = parse.quote(search_string)
        return 'https://www.google.com/maps/search/?api=1&query=' + search_string
