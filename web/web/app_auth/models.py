from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .custom_user_manager import UserManager
from .validators import validate_only_digits


def create_groups(self):
    # Create the "Doctors" group
    doctors_group, _ = Group.objects.get_or_create(name='Doctors')

    # Create the "Patients" group
    patients_group, _ = Group.objects.get_or_create(name='Patients')


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


class ChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]


class Genders(ChoicesEnum):
    male = 'Male'
    female = 'Female'
    other = 'other'


class Stages(ChoicesEnum):
    I = 'I'
    II = 'II'
    III = 'III'
    IV = 'IV'


class HER2(ChoicesEnum):
    plus = '+'
    two_plus = '++'
    three_plus = '+++'


class ER(ChoicesEnum):
    positive = '+'
    negative = '-'


class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, validators=(validate_only_digits,))
    civil_number = models.CharField(max_length=10, null=True, blank=True, validators=(validate_only_digits,))
    gender = models.CharField(max_length=6, choices=Genders.choices(), null=True, blank=True, )

    def __str__(self):
        if self.first_name is None or self.middle_name is None or self.last_name is None:
            return f'{self.user.email}'
        return f'{self.first_name} {self.middle_name} {self.last_name} / {self.civil_number}'

    class Meta:
        verbose_name = "PatientProfile"
        verbose_name_plural = "PatientProfiles"

    def get_full_name(self):
        """
        Return the first_name the middle_name and the last_name, with a space in between.
        """
        full_name = "%s %s %s" % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()

    def get_details(self):
        return [self.phone_number, self.civil_number, self.gender]


class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True, validators=(validate_only_digits,))
    uin_number = models.CharField(max_length=20, null=True, blank=True, validators=(validate_only_digits,))
    specialization = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()

    gender = models.CharField(max_length=6, choices=Genders.choices(), null=True, blank=True, )

    def __str__(self):
        if self.first_name is None or self.middle_name is None or self.last_name is None:
            return f'{self.user.email}'
        return f'MD. {self.first_name} {self.middle_name} {self.last_name}'

    class Meta:
        verbose_name = "DoctorProfile"
        verbose_name_plural = "DoctorProfiles"


class OncologyStatus(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    histology_diagnose = models.TextField(blank=False, null=False, )
    tnm = models.CharField(max_length=30, blank=False, null=False, verbose_name='TNM')
    stage = models.CharField(max_length=10, choices=Stages.choices(), blank=False, null=False)
    her2 = models.CharField(max_length=15, choices=HER2.choices(), blank=False, null=False, verbose_name='HER2')
    er = models.CharField(max_length=15, choices=ER.choices(), blank=False, null=False, verbose_name='ER')
    pr = models.CharField(max_length=15, choices=ER.choices(), blank=False, null=False, verbose_name='PR')
    ki_67 = models.PositiveIntegerField(blank=False, null=False, verbose_name='KI 67')
    start_date = models.DateTimeField(blank=False, null=False, auto_now_add=True)

    def __str__(self):

        return f'{self.histology_diagnose}'

    class Meta:
        verbose_name = "OncologyStatus"
        verbose_name_plural = "OncologyStatuses"
