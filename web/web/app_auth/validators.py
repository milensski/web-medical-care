from django.core import exceptions
from django.utils.translation import gettext as _


def validate_only_digits(value):
    if not value.isdigit():
        raise exceptions.ValidationError(_(f"Invalid value '{value}' must contain only digits"))



