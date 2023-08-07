from django.core import exceptions
from django.utils.translation import gettext as _


def validate_only_digits(value):
    if not value.isdigit():
        raise exceptions.ValidationError(_(f"Invalid '{value}' must contain only digits"))


def validate_only_chars(value):
    for char in value:
        if not char.isalpha() and not char.isspace():
            raise exceptions.ValidationError(_(f"Invalid '{value}' must contain only characters"))
