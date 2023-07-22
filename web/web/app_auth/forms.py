from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from web.app_auth.models import DoctorProfile, PatientProfile, Appointment, AppointmentPoll, TherapyPlan
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


class LandingPageSignInForm(SignInForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and placeholders to the form fields
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter your email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter your password'})

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            # Validate email format using Django's built-in validator
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError('Invalid email format.')

            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


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


class AppointmentPollForm(forms.ModelForm):
    class Meta:
        model = AppointmentPoll
        fields = (
            'current_condition', 'high_temperature', 'cough', 'sores_in_mouth', 'sores_in_nose', 'cold', 'diarrhea',
            'skin_rash', 'additional_info')
        widgets = {
            'additional_info': forms.Textarea(attrs={'rows': 4}),
        }


class TreatmentPlanForm(forms.ModelForm):
    # medications = forms.ModelMultipleChoiceField(
    #     queryset=Medication.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     required=True,
    # )

    class Meta:
        model = TherapyPlan
        fields = ['medication', 'dosage', 'duration_days', 'instructions']


class UpdateTreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TherapyPlan
        fields = ['medication', 'dosage', 'duration_days', 'instructions']
