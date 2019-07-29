from django.test import TestCase

from apps.profile.models.totem import Totem


class TotemTestCase(TestCase):

    kleurentotem = 'zonnebloemgroene'
    kleurentotem_text = 'Kleurentotem beschrijving'
    voortotem = 'joviale'
    voortotem_text = 'Voortotem beschrijving'
    totem = 'ezel'
    totem_text = 'Totem beschrijving'

    def test_creation_should_convert_all_totem_parts_to_lower_case(self):
        # Build
        totem = Totem.objects.create(
            kleurentotem=self.kleurentotem.upper(),
            kleurentotem_text=self.kleurentotem_text,
            voortotem=self.voortotem.upper(),
            voortotem_text=self.voortotem_text,
            totem=self.totem.upper(),
            totem_text=self.totem_text
        )

        # Check
        self.assertEqual(
            totem.kleurentotem,
            self.kleurentotem,
            'Color totem should be converted to lower case'
        )
        self.assertEqual(
            totem.voortotem,
            self.voortotem,
            'Voortotem should be converted to lower case'
        )
        self.assertEqual(
            totem.totem,
            self.totem,
            'Totem should be converted to lower case'
        )

    def test_str_method_only_totem(self):
        # Build
        totem = Totem.objects.create(
            totem=self.totem,
            totem_text=self.totem_text
        )
        # Operate
        to_string = str(totem)

        # Check
        self.assertEqual(
            to_string,
            f'{self.totem}',
            'String method should be something sensible'
        )

    def test_str_method_totem_and_voortotem(self):
        # Build
        totem = Totem.objects.create(
            voortotem=self.voortotem,
            voortotem_text=self.voortotem_text,
            totem=self.totem,
            totem_text=self.totem_text
        )
        # Operate
        to_string = str(totem)

        # Check
        self.assertEqual(
            to_string,
            f'{self.voortotem} {self.totem}',
            'String method should be something sensible'
        )

    def test_str_method_everything(self):
        # Build
        totem = Totem.objects.create(
            kleurentotem=self.kleurentotem,
            kleurentotem_text=self.kleurentotem_text,
            voortotem=self.voortotem,
            voortotem_text=self.voortotem_text,
            totem=self.totem,
            totem_text=self.totem_text
        )
        # Operate
        to_string = str(totem)

        # Check
        self.assertEqual(
            to_string,
            f'{self.kleurentotem} {self.voortotem} {self.totem}',
            'String method should be something sensible'
        )

    def test_str_method_totem_and_colortotem(self):
        # Build
        totem = Totem.objects.create(
            kleurentotem=self.kleurentotem,
            kleurentotem_text=self.kleurentotem_text,
            totem=self.totem,
            totem_text=self.totem_text
        )
        # Operate
        to_string = str(totem)

        # Check
        self.assertEqual(
            to_string,
            f'{self.kleurentotem} {self.totem}',
            'String method should be something sensible'
        )

    def test_str_method_everything_empty(self):
        # Build
        totem = Totem.objects.create()
        # Operate
        to_string = str(totem)

        # Check
        self.assertEqual(
            to_string,
            '',
            'String method should be something sensible'
        )
