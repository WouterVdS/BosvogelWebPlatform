from django.test import TestCase

from apps.place.models import Place


class PlaceTestCase(TestCase):

    def setUp(self):
        Place.objects.create(
            name='De Rimboe',
            country='Belgium',
            zipcode='2280',
            city='Grobbendonk',
            street_and_number='Kremersgat 2',
        )
        Place.objects.create(
            name='Camping ground',
            latitude=50.44246,
            longitude=5.04035
        )

    def test_str_method(self):
        # Check
        self.assertEqual(str(Place.objects.get(name='De Rimboe')),
                         'De Rimboe, Kremersgat 2, 2280, Grobbendonk, Belgium',
                         'String method should be something sensible')
        self.assertEqual(str(Place.objects.get(name='Camping ground')),
                         'Camping ground,  lat: 50.442460, long: 5.040350',
                         'String method should be something sensible')

    def test_link_to_maps(self):
        # Operate
        address = Place.objects.get(name='De Rimboe')
        latlong = Place.objects.get(name='Camping ground')

        # Check
        self.assertEqual(address.link_to_maps(),
                         'https://www.google.com/maps/search/?api=1&query=Kremersgat%202%2C%202280%20Grobbendonk',
                         'The link should be a correct Google Maps link')
        self.assertEqual(latlong.link_to_maps(),
                         'https://www.google.com/maps/search/?api=1&query=50.442460,5.040350',
                         'The link should be a correct Google Maps link')
