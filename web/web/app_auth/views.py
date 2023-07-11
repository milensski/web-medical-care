from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .decorators import restrict_profile_type, redirect_authenticated_user
from .forms import SignInForm, CustomUserForm, ProfileTypeForm, DoctorProfileForm, PatientProfileForm
from .mixins import LoggedUserRedirectMixin
from .models import DoctorProfile, PatientProfile


@redirect_authenticated_user
def registration_step1(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user object
            login(request, user)  # Log in the user
            return redirect('registration step2')
    else:
        form = CustomUserForm()
    return render(request, 'registration_step1.html', {'form': form})


@login_required()
@redirect_authenticated_user
def registration_step2(request):
    if request.method == 'POST':
        form = ProfileTypeForm(request.POST)
        if form.is_valid():
            profile_type = form.cleaned_data['profile_type']
            request.session['profile_type'] = profile_type
            if profile_type == 'doctor':
                return redirect('doctor profile')
            elif profile_type == 'patient':
                return redirect('patient profile')
    else:
        form = ProfileTypeForm()
    return render(request, 'registration_step2.html', {'form': form})


@login_required()
@restrict_profile_type
def doctor_profile(request):
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            doctors_group = Group.objects.get(name='Doctors')
            request.user.groups.add(doctors_group)

            return redirect('index')
    else:
        form = DoctorProfileForm()
    return render(request, 'doctor_profile.html', {'form': form})


@login_required()
@restrict_profile_type
def patient_profile(request):
    if request.method == 'POST':
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            patient_group = Group.objects.get(name='Patients')
            request.user.groups.add(patient_group)
            return redirect('index')
    else:
        form = PatientProfileForm()
    return render(request, 'patient_profile.html', {'form': form})


class SignInView(LoggedUserRedirectMixin, LoginView):
    form_class = SignInForm
    template_name = 'signin.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.get_user()

        print(login(self.request, user))

        return super().form_valid(form)


class SignOutView(LogoutView):
    pass


@login_required
def index(request):
    user = request.user
    profile = None
    is_doctor = False

    try:
        if user.groups.filter(name='Doctors').exists():
            profile = DoctorProfile.objects.get(user=user)
            is_doctor = True
        elif user.groups.filter(name='Patients').exists():
            profile = PatientProfile.objects.get(user=user)
    except (DoctorProfile.DoesNotExist, PatientProfile.DoesNotExist):
        # Profile does not exist
        pass

    context = {
        'profile': profile,
        'is_doctor': is_doctor,
    }

    return render(request, 'index.html', context)
