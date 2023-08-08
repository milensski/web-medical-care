from django.contrib import admin
from django.contrib.auth import get_user_model

from web.app_auth.models import PatientProfile, DoctorProfile, Medication, Appointment, AppointmentPoll, TherapyPlan, \
    OncologyStatus

# Register your models here.
UserModel = get_user_model()


@admin.register(UserModel)
class UsersAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']
    list_display = ('email', 'img_preview')
    search_fields = ("email",)
    search_help_text = 'Search for email'


@admin.register(PatientProfile)
class PatientProfilesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'civil_number', 'phone_number',)
    search_fields = ('first_name', 'middle_name', 'last_name', 'civil_number', 'phone_number')
    search_help_text = 'Search by Name, PIN or Phone'
    list_filter = ('gender',)


@admin.register(DoctorProfile)
class DoctorProfilesAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'uin_number', 'specialization', 'experience',)
    search_fields = ('first_name', 'middle_name', 'last_name', 'uin_number',)
    search_help_text = 'Search by Name or UIN'
    list_filter = ('gender',)


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'for_date', 'for_time', 'status')
    list_filter = ('status', 'for_date', 'for_time')


@admin.register(AppointmentPoll)
class AppointmentPollAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'current_condition', 'additional_info')
    list_filter = ('current_condition',)


@admin.register(TherapyPlan)
class TherapyPlanAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'medication', 'dosage', 'duration_days')
    search_fields = ("medication",)
    search_help_text = 'Search by medication'


@admin.register(OncologyStatus)
class OncologyStatusAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'histology_diagnose', 'tnm', 'stage', 'her2', 'start_date')
    list_filter = ('start_date',)