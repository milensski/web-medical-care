from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .custom_user_manager import UserManager
from .validators import validate_only_digits


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False, null=False, validators=(EmailValidator,))
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    civil_number = models.CharField(max_length=10, null=True, blank=True, validators=(validate_only_digits,))

    def __str__(self):
        if self.first_name is None or self.middle_name is None or self.last_name is None:
            return f'{self.user.email}'
        return f'{self.first_name} {self.middle_name} {self.last_name}'

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
