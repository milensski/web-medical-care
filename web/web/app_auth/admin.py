from django.contrib import admin
from django.contrib.auth import get_user_model

from web.app_auth.models import PatientProfile, DoctorProfile

# Register your models here.
UserModel = get_user_model()


@admin.register(UserModel)
class UsersAdmin(admin.ModelAdmin):
    pass


@admin.register(PatientProfile)
class PatientProfilesAdmin(admin.ModelAdmin):
    pass


@admin.register(DoctorProfile)
class DoctorProfilesAdmin(admin.ModelAdmin):
    pass
