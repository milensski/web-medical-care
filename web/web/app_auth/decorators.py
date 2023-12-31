from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import DoctorProfile, PatientProfile


def restrict_profile_type(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = request.user
        existing_doctor_profile = DoctorProfile.objects.filter(user=user).exists()
        existing_patient_profile = PatientProfile.objects.filter(user=user).exists()

        if existing_doctor_profile or existing_patient_profile:
            # User has already created both profiles, display an error message or redirect
            return redirect('index')  # Replace 'error_page' with the desired URL or view
        elif existing_doctor_profile and 'patient' in request.path:
            # User has already created a doctor profile, redirect or display a message
            return redirect('index')  # Replace 'error_page' with the desired URL or view
        elif existing_patient_profile and 'doctor' in request.path:
            # User has already created a patient profile, redirect or display a message
            return redirect('index')  # Replace 'error_page' with the desired URL or view

        return view_func(request, *args, **kwargs)

    return wrapper


def redirect_authenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='Doctors').exists():
            # User is already logged in, redirect to a different page
            return redirect('index')  # Replace 'home' with the desired URL or view

        elif request.user.is_authenticated and request.user.groups.filter(name='Patients').exists():
            # User is already logged in, redirect to a different page
            return redirect('index')  # Replace 'home' with the desired URL or view

        return view_func(request, *args, **kwargs)

    return wrapper


def doctor_or_self_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.groups.filter(name='Doctors').exists() and user.pk != kwargs.get('pk'):
            return redirect("index")
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view


def patient_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if user.groups.filter(name='Doctors').exists():
            return redirect("index")
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view


def doctor_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.groups.filter(name='Doctors').exists():
            return redirect("index")
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view
