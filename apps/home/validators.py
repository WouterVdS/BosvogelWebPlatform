import re

from django.core.exceptions import ValidationError


def validate_international_phone_number(value):
    if not value.startswith('0032'):
        raise ValidationError(f'Gsmnummer moet beginnen met 0032')


def validate_iban_format(value):
    pattern = re.compile(r'[A-Z]{2}\d{2} ?\d{4} ?\d{4} ?\d{4} ?[\d]{0,2}')
    if not pattern.match(value):
        raise ValidationError(f'Rekeningnummer moet in het volgende formaat staan: BExx xxxx xxxx xxxx')
