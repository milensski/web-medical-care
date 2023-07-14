from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView

from .decorators import restrict_profile_type, redirect_authenticated_user
from .filters import PatientFilter
from .forms import SignInForm, CustomUserForm, ProfileTypeForm, DoctorProfileForm, PatientProfileForm
from .mixins import LoggedUserRedirectMixin, DoctorRequiredMixin
from .models import DoctorProfile, PatientProfile, OncologyStatus


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


class DoctorDashboard(DoctorRequiredMixin, ListView):
    model = PatientProfile
    template_name = 'doctor_dashboard.html'
    context_object_name = 'patients'
    ordering = ['-pk']


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patients_with_oncology = []
        patients_without_oncology = []
        myFilter = PatientFilter(self.request.GET, queryset=self.queryset)
        context['patients'] = myFilter.qs
        for patient in context['patients']:
            oncology_status = OncologyStatus.objects.filter(patient_id=patient.pk).first()

            if oncology_status:
                patients_with_oncology.append((patient, oncology_status))
            else:
                patients_without_oncology.append(patient)

        context['myFilter'] = myFilter
        context['patients_with_oncology'] = patients_with_oncology
        context['patients_without_oncology'] = patients_without_oncology
        return context

    """
    The get_queryset() method is overridden to filter the patient profiles 
    based on the logged-in doctor. 
    It retrieves only the patient profiles that have a foreign key relationship 
    with the logged-in doctor.
    
    """
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(doctor__user=self.request.user)


class AddOncologyStatus(DoctorRequiredMixin, CreateView):
    template_name = 'add_oncology_status.html'
    model = OncologyStatus
    fields = '__all__'
    success_url = reverse_lazy('doctor dashboard')

    def get_initial(self):
        initial = super().get_initial()
        print(self.request.user.pk)
        initial['doctor'] = DoctorProfile.objects.get(pk=13)  # HARD CODED since the user must be doctor
        initial['patient'] = self.get_patient()
        return initial

    def form_valid(self, form):
        # Check if an OncologyStatus record already exists for the doctor and patient combination
        existing_status = OncologyStatus.objects.filter(
            doctor=form.cleaned_data['doctor'],
            patient=form.cleaned_data['patient']
        ).exists()

        if existing_status:
            # Redirect or display an error message indicating that the status already exists
            # You can modify the behavior based on your requirements
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_doctor(self):
        doctor = DoctorProfile.objects.get(self.request.user)
        return doctor

    def get_patient(self):
        patient = PatientProfile.objects.get(pk=self.kwargs['pk'])
        return patient


class UpdateOncologyStatus(DoctorRequiredMixin, UpdateView):
    template_name = 'update_oncology_status.html'
    model = OncologyStatus
    fields = '__all__'
    success_url = reverse_lazy('doctor dashboard')

    def get_object(self, queryset=None):
        patient_id = self.kwargs['pk']
        oncology_status_id = self.kwargs['onco_status']
        obj = self.model.objects.get(patient__pk=patient_id, pk=oncology_status_id)
        return obj


class ViewOncologyStatus(DetailView):
    template_name = 'view_oncology_status.html'
    model = OncologyStatus
    context_object_name = 'oncology_status'

    def get_object(self, queryset=None):
        patient_id = self.kwargs['pk']
        oncology_status_id = self.kwargs['onco_status']
        obj = self.model.objects.get(patient__pk=patient_id, pk=oncology_status_id)
        return obj


class PatientProfileDetails(LoginRequiredMixin, DetailView):
    model = PatientProfile
    template_name = 'patient_profile_details.html'
    context_object_name = 'patient'


class PatientProfileEdit(LoginRequiredMixin, UpdateView):
    model = PatientProfile
    fields = ('first_name', 'middle_name', 'last_name', 'phone_number', 'civil_number', 'gender')
    template_name = 'patient_profile_edit.html'
    success_url = reverse_lazy('doctor dashboard')  # Replace with the desired URL or reverse('dashboard')
    ordering = ['pk']