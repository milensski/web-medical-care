from django.core import exceptions


def validate_only_digits(value):

    if not value.isdigit():
        raise exceptions.ValidationError('Ensure this value contains only letters, numbers, and underscore.')
