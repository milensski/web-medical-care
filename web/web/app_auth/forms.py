from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from web.app_auth.models import DoctorProfile, PatientProfile, Appointment, AppointmentPoll, TherapyPlan, OncologyStatus
from .widgets import DatePickerInput

UserModel = get_user_model()


class ProfileTypeForm(forms.Form):
    profile_type = forms.ChoiceField(
        choices=[('doctor', 'Doctor'), ('patient', 'Patient')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )


class CustomUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter your email'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter your password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Repeat your password'})

    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2')


class DoctorProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter first name'})
        self.fields['middle_name'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter middle name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter last name'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter phone number'})
        self.fields['uin_number'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter UIN number'})
        self.fields['specialization'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter field of specialization'})
        self.fields['experience'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter years of experience'})

    class Meta:
        model = DoctorProfile
        fields = (
            'first_name', 'middle_name', 'last_name', 'phone_number', 'uin_number', 'specialization', 'experience',
            'gender')


class PatientProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and placeholders to the form fields
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter first name'})
        self.fields['middle_name'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter middle name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter last name'})
        self.fields['phone_number'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter phone number'})
        self.fields['civil_number'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter personal id number'})

    class Meta:
        model = PatientProfile
        fields = ('first_name', 'middle_name', 'last_name', 'civil_number', 'phone_number', 'gender')


class SignInForm(AuthenticationForm):
    class Meta:
        fields = ('email', 'password')


class LandingPageSignInForm(SignInForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter your email', 'type': 'email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control2 text-center', 'placeholder': 'Enter your password'})

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
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


class OncologyStatusForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['doctor'].widget = forms.HiddenInput()
        self.fields['patient'].widget = forms.HiddenInput()

    class Meta:
        model = OncologyStatus
        fields = '__all__'


class AppointmentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patient'].widget.attrs['hidden'] = True
        self.fields['for_date'].widget.attrs.update({'class': 'form-control', })
        self.fields['for_time'].widget.attrs.update({'class': 'form-control'})
        self.fields['symptoms'].widget.attrs.update({'class': 'form-control', 'rows': 4})
        self.fields['doctor'].widget.attrs.update({'class': 'custom-select'})

    def clean(self):
        cleaned_data = super().clean()
        for_date = cleaned_data.get('for_date')
        for_time = cleaned_data.get('for_time')
        doctor = cleaned_data.get('doctor')

        if for_date and for_time and doctor:
            existing_appointment = Appointment.objects.filter(
                for_date=for_date,
                for_time=for_time,
                doctor=doctor
            ).exclude(pk=self.instance.pk if self.instance else None).first()

            if existing_appointment:
                raise forms.ValidationError(
                    "An appointment already exists for the selected date and time."
                )
        return cleaned_data

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
        exclude = ('status',)
        model = Appointment

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['patient'].widget = forms.HiddenInput()


class AppointmentPollForm(forms.ModelForm):
    class Meta:
        model = AppointmentPoll
        fields = (
            'current_condition', 'high_temperature', 'cough', 'sores_in_mouth', 'sores_in_nose', 'cold', 'diarrhea',
            'skin_rash', 'additional_info')
        widgets = {

            'additional_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TherapyPlan
        fields = ['medication', 'dosage', 'duration_days', 'instructions']


class UpdateTreatmentPlanForm(forms.ModelForm):
    class Meta:
        model = TherapyPlan
        fields = ['medication', 'dosage', 'duration_days', 'instructions']
