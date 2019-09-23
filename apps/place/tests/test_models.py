from django.test import TestCase

from apps.place.models import Place


class PlaceTestCase(TestCase):

    def setUp(self):
        Place.objects.create(
            name='De Rimboe',
            country='Ons Landje',
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
                         'De Rimboe, Kremersgat 2, 2280, Grobbendonk, Ons Landje',
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

    def test_it_should_not_show_the_country_when_it_is_Belgium(self):
        # Build
        belgium_synonyms = ['België', 'belgië', 'Belgium', 'belgium', 'Belgie', 'België']

        for synonym in belgium_synonyms:
            Place.objects.create(
                name='Testlocatie',
                country=synonym,
                zipcode='2280',
                city='Grobbendonk',
                street_and_number='Kremersgat 2',
            )

        # Operate
        result = ','.join([str(x) for x in Place.objects.all()])

        # Check
        self.assertFalse('elg' in result.lower(),
                         'When the country is Belgium (or one if the ways you can write it),'
                         'it should not be in the string representation. But it is displayed :' + result)
