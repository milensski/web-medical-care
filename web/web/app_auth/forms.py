from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from web.app_auth.models import DoctorProfile, PatientProfile, Appointment
from .widgets import DatePickerInput

UserModel = get_user_model()


class CustomUserForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2')


class ProfileTypeForm(forms.Form):
    profile_type = forms.ChoiceField(
        choices=[('doctor', 'Doctor'), ('patient', 'Patient')],
        widget=forms.RadioSelect,
        required=True
    )


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = (
            'first_name', 'middle_name', 'last_name', 'phone_number', 'uin_number', 'specialization', 'experience',
            'gender')


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ('first_name', 'middle_name', 'last_name', 'phone_number', 'civil_number', 'gender')


class SignInForm(AuthenticationForm):
    class Meta:
        fields = ('email', 'password')


class SignOutForm(forms.Form):
    pass


class AppointmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs['hidden'] = True


    class Meta:
        model = Appointment
        exclude = ('status',)

        widgets = {
            'for_date': DatePickerInput(),
        }
        labels = {
            "patient": ""
        }

class UpdateAppointmentForm(forms.ModelForm):
    status = forms.ChoiceField

    class Meta:
        fields = '__all__'
        model = Appointment

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget = forms.Select(choices=Appointment.STATUS, attrs={'class': 'form-control'})
