from django.contrib.auth.models import AbstractUser
from django.db import models

from .custom_user_manager import UserManager


class CustomUser(AbstractUser):
    objects = UserManager()

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_doctor = models.BooleanField(default=False)
    specialization = models.CharField(max_length=150, blank=True, null=True)
    personal_info = models.TextField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_staff = True

        super().save(*args, **kwargs)

    def promote_to_doctor(self):
        self.is_doctor = True
        self.save()
