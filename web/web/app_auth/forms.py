from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from web.app_auth.models import DoctorProfile, PatientProfile

UserModel = get_user_model()


# class SignUpForm(UserCreationForm):
#     username = forms.CharField(max_length=30, required=True, )
#     first_name = forms.CharField(max_length=30, required=True, )
#     last_name = forms.CharField(max_length=30, required=True, )
#     email = forms.EmailField(max_length=254, required=True, )
#     password1 = forms.CharField(
#         label=_("Password"),
#         strip=False,
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#         help_text='Please use strong password',
#     )
#     password2 = forms.CharField(
#         label=_("Password confirmation"),
#         widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
#         strip=False,
#         help_text=_("Repeat password"),
#     )
#
#     class Meta:
#         model = UserModel
#         fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


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
