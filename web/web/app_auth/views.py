from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView, LogoutView
from django.core.files.storage import default_storage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .decorators import redirect_authenticated_user, restrict_profile_type, patient_required, doctor_required
from .filters import PatientFilter, AppointmentFilter
from .forms import CustomUserForm, ProfileTypeForm, DoctorProfileForm, PatientProfileForm, AppointmentForm, \
    AppointmentPollForm, TreatmentPlanForm, UpdateTreatmentPlanForm, SignInForm, UpdateAppointmentForm, \
    LandingPageSignInForm, OncologyStatusForm
from .functions import show_errors
from .mixins import LoggedUserRedirectMixin, DoctorRequiredMixin, DoctorOrSelfRequiredMixin, SelfRequiredMixin
from .models import DoctorProfile, PatientProfile, OncologyStatus, Appointment, TherapyPlan

UserModel = get_user_model()


class LandingPageView(LoggedUserRedirectMixin, LoginView):
    form_class = LandingPageSignInForm
    template_name = 'index.html'
    success_url = reverse_lazy('landing page')

    def form_valid(self, form):
        user = form.get_user()

        login(self.request, user)

        return super().form_valid(form)


@login_required
def index(request):
    user = request.user

    if request.user.is_superuser:
        return redirect('/admin')

    try:
        if user.groups.filter(name='Doctors').exists():
            profile = DoctorProfile.objects.get(user=user)
            return redirect('doctor dashboard')
        elif user.groups.filter(name='Patients').exists():
            profile = PatientProfile.objects.get(user=user)
            return redirect('patient dashboard')

    except (DoctorProfile.DoesNotExist, PatientProfile.DoesNotExist):
        print('Profile does not exist!')
        return render(request, '404.html', )

    return redirect('landing page')


@redirect_authenticated_user
def registration_step1(request):
    form = CustomUserForm()

    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('registration step2')
        else:
            show_errors(request, form)

    return render(request, 'registration_step1.html', {'form': form})


@login_required()
@redirect_authenticated_user
def registration_step2(request):
    if request.method == 'POST':
        form = ProfileTypeForm(request.POST)
        print(form)
        if form.is_valid():
            profile_type = form.cleaned_data['profile_type']
            print(profile_type)
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
    form = DoctorProfileForm()

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
            show_errors(request, form)

    return render(request, 'doctor_profile.html', {'form': form})


@login_required()
@restrict_profile_type
def patient_profile(request):
    form = PatientProfileForm()

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
            show_errors(request, form)

    return render(request, 'patient_profile.html', {'form': form})


class UserProfilePictureChange(SelfRequiredMixin, UpdateView):
    model = UserModel
    fields = ('profile_picture',)
    template_name = 'picture_profile_edit.html'
    ordering = ['pk']

    def get_success_url(self):
        pk = self.kwargs['pk']
        if DoctorProfile.objects.filter(pk=pk).exists():
            return reverse_lazy('doctor details', kwargs={'pk': pk})
        return reverse_lazy('patient details', kwargs={'pk': pk})

    def form_valid(self, form):
        if not form.cleaned_data['profile_picture']:
            try:
                old_img = form.initial['profile_picture']
                if old_img and default_storage.exists(old_img.name):
                    default_storage.delete(old_img.name)
            except (AttributeError, ValueError):
                pass
        else:
            try:
                old_img = form.initial['profile_picture']
                new_img = form.cleaned_data['profile_picture']
                if old_img != new_img:
                    default_storage.delete(old_img.name)

            except (AttributeError, ValueError):
                pass

        return super().form_valid(form)


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


@patient_required
def patient_dashboard(request):
    patient = PatientProfile.objects.filter(user=request.user).first()

    appointments = Appointment.objects.filter(patient=patient).filter(status='Pending')
    oncology_status = OncologyStatus.objects.filter(patient=patient).first()
    treatment = TherapyPlan.objects.filter(patient=patient).first()

    context = {
        'patient': patient,
        'oncology_status': oncology_status,
        'appointments': appointments,
        'treatment': treatment
    }

    return render(request, 'patient_dashboard.html', context)


class PatientProfileDetails(LoginRequiredMixin, DetailView):
    model = PatientProfile
    template_name = 'patient_profile_details.html'
    context_object_name = 'patient'


class PatientProfileEdit(DoctorOrSelfRequiredMixin, UpdateView):
    model = PatientProfile
    fields = ('first_name', 'middle_name', 'last_name', 'phone_number', 'civil_number', 'gender',)
    template_name = 'patient_profile_edit.html'
    ordering = ['pk']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('patient details', kwargs={'pk': pk})


@patient_required
def schedule_appointment(request):
    patient = PatientProfile.objects.filter(user=request.user).get()

    form = AppointmentForm(initial={'patient': patient})

    if request.method == 'POST':
        form = AppointmentForm(request.POST, initial={'patient': patient})
        if form.is_valid():
            appointment = form.save()
            request.session['appointment.pk'] = appointment.pk
            return redirect('create appointment poll')
        else:
            messages.add_message(request, level=messages.ERROR,
                                 message='An appointment already exists for the selected date and time.')
    context = {
        'form': form
    }

    return render(request, 'schedule_appointment.html', context)


@patient_required
def cancel_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    if request.user.pk == appointment.patient.pk:
        appointment.status = 'Canceled'
        appointment.save()
        return redirect('view appointment', pk=pk)

    messages.add_message(request, level=messages.ERROR,
                         message='You are not authorized to cancel another user appointment')

    return redirect('view appointment', pk=pk)


@doctor_required
def reject_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    appointment.status = 'Rejected'
    appointment.save()
    return redirect('view appointment', pk=pk)


@doctor_required
def approve_appointment(request, pk):
    appointment = Appointment.objects.get(pk=pk)
    print(appointment)
    appointment.status = 'Approved'
    appointment.save()
    return redirect('view appointment', pk=pk)


@doctor_required
def delete_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.add_message(request, level=messages.SUCCESS, message='Successfully deleted')
    return redirect('doctor dashboard')


class ViewAppointment(LoginRequiredMixin, DetailView):
    model = Appointment
    template_name = 'appointment_details.html'
    context_object_name = 'appointment'


class UpdateAppointment(LoginRequiredMixin, UpdateView):
    template_name = 'update_appointment_status.html'
    model = Appointment
    form_class = UpdateAppointmentForm

    def get(self, request, *args, **kwargs):
        patient = Appointment.objects.filter(pk=kwargs['pk']).get().patient
        doctor = Appointment.objects.filter(pk=kwargs['pk']).get().doctor
        if request.user.pk == patient.pk or request.user.pk == doctor.pk:
            return super().get(request, *args, **kwargs)
        return redirect('index')

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('view appointment', kwargs={'pk': pk})


class BaseHistoryAppointments(ListView):
    template_name = 'history_appointments.html'
    model = Appointment
    context_object_name = 'appointments'
    ordering = ['pk']
    paginate_by = 10


class HistoryAppointments(DoctorRequiredMixin, BaseHistoryAppointments):

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset \
            .exclude(status='Pending')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_filter = AppointmentFilter(self.request.GET, queryset=self.get_queryset())
        paginator = Paginator(my_filter.qs, self.paginate_by)
        page_number = self.request.GET.get('page')
        appointments = paginator.get_page(page_number)

        context['appointments'] = appointments
        context['my_filter'] = my_filter
        return context


class PatientHistoryAppointment(DoctorOrSelfRequiredMixin, LoginRequiredMixin, BaseHistoryAppointments):
    def get_queryset(self):
        patient_pk = self.kwargs['pk']
        queryset = super().get_queryset()
        queryset = queryset \
            .filter(patient=patient_pk) \
            .exclude(status='Pending')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointment = self.get_queryset()
        paginator = Paginator(appointment, self.paginate_by)
        page_number = self.request.GET.get('page')
        appointments = paginator.get_page(page_number)

        context['appointments'] = appointments
        return context


@patient_required
def create_appointment_poll(request):
    appointment = Appointment.objects.get(pk=request.session['appointment.pk'])
    if request.method == 'POST':
        form = AppointmentPollForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.appointment = appointment
            poll.save()
            messages.add_message(request, level=messages.SUCCESS,
                                 message='Successfully created appointment')
            return redirect('view appointment', pk=appointment.pk)
    else:
        form = AppointmentPollForm()

    context = {
        'form': form,
        'appointment': appointment,
    }
    return render(request, 'create_appointment_poll.html', context)


@doctor_required
def create_treatment_plan(request, patient_pk):
    patient = PatientProfile.objects.get(pk=patient_pk)

    if request.method == 'POST':
        form = TreatmentPlanForm(request.POST)
        if form.is_valid():
            treatment_plan = form.save(commit=False)
            treatment_plan.patient = patient
            treatment_plan.save()
            form.save_m2m()  # Save the medications many-to-many relationship
            return redirect('view treatment plan', treatment_plan_pk=treatment_plan.pk)
    else:
        form = TreatmentPlanForm()

    context = {
        'patient': patient,
        'form': form,
    }

    return render(request, 'create_treatment_plan.html', context)


@login_required()
def view_treatment_plan(request, treatment_plan_pk):
    treatment_plan = TherapyPlan.objects.get(pk=treatment_plan_pk)

    user = request.user

    if not user.groups.filter(name='Doctors').exists() and user.pk != treatment_plan.patient.pk:
        return redirect('index')

    context = {
        'treatment_plan': treatment_plan,
    }

    return render(request, 'treatment_plan_details.html', context)


@doctor_required
def update_treatment_plan(request, treatment_plan_pk):
    treatment = TherapyPlan.objects.get(pk=treatment_plan_pk)

    if request.method == 'POST':
        form = UpdateTreatmentPlanForm(request.POST, instance=treatment)
        if form.is_valid():
            form.save()
            return redirect('view treatment plan',
                            treatment_plan_pk=treatment.pk)
    else:
        form = UpdateTreatmentPlanForm(instance=treatment)

    context = {
        'form': form,
        'treatment_plan': treatment,
    }

    return render(request, 'treatment_plan_edit.html', context)


class DoctorDashboard(DoctorRequiredMixin, ListView):
    model = PatientProfile
    template_name = 'doctor_dashboard.html'
    context_object_name = 'patients'
    # ordering = ''
    queryset = PatientProfile.objects.all().order_by('first_name', 'last_name', 'pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = DoctorProfile.objects.filter(user=self.request.user).get()
        patients_with_oncology = []
        patients_without_oncology = []
        patients_with_therapy = []
        patients_without_therapy = []
        my_filter = PatientFilter(self.request.GET, queryset=self.queryset)
        context['patients'] = my_filter.qs
        for patient in context['patients']:
            oncology_status = OncologyStatus.objects.filter(patient_id=patient.pk).first()
            therapy = TherapyPlan.objects.filter(patient_id=patient.pk).first()
            if oncology_status:
                patients_with_oncology.append((patient, oncology_status))
            else:
                patients_without_oncology.append(patient)

            if therapy:
                patients_with_therapy.append((patient, therapy))
            else:
                patients_without_therapy.append(patient)

        appointments = Appointment.objects.filter(doctor=doctor).filter(status='Pending').all().order_by('patient_id')
        paginator = Paginator(appointments, 2)
        page = self.request.GET.get('page')

        try:
            appointments = paginator.page(page)
        except PageNotAnInteger:
            appointments = paginator.page(1)
        except EmptyPage:
            appointments = paginator.page(paginator.num_pages)

        context['appointments'] = appointments
        context['my_filter'] = my_filter
        context['patients_with_oncology'] = patients_with_oncology
        context['patients_without_oncology'] = patients_without_oncology
        context['patients_with_therapy'] = patients_with_therapy
        context['patients_without_therapy'] = patients_without_therapy
        context['page_obj'] = appointments
        context['paginator'] = paginator
        return context


class DoctorProfileDetails(LoginRequiredMixin, DetailView):
    model = DoctorProfile
    template_name = 'doctor_profile_details.html'
    context_object_name = 'doctor'


class DoctorProfileEdit(SelfRequiredMixin, UpdateView):
    model = DoctorProfile
    fields = ('first_name', 'middle_name', 'last_name', 'phone_number', 'uin_number', 'specialization', 'experience')
    template_name = 'doctor_profile_edit.html'
    ordering = ['pk']

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('doctor details', kwargs={'pk': pk})


class AddOncologyStatus(DoctorRequiredMixin, CreateView):
    template_name = 'add_oncology_status.html'
    model = OncologyStatus
    form_class = OncologyStatusForm

    def get_initial(self):
        initial = super().get_initial()
        print(self.request.user.pk)
        initial['doctor'] = DoctorProfile.objects.get(pk=self.get_doctor().pk)
        initial['patient'] = self.get_patient()
        return initial

    def form_valid(self, form):
        existing_status = OncologyStatus.objects.filter(
            doctor=form.cleaned_data['doctor'],
            patient=form.cleaned_data['patient']
        ).exists()

        if existing_status:
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        onco_status_pk = self.object.pk
        patient = self.get_patient()
        return reverse_lazy('view oncology status', kwargs={'onco_status': onco_status_pk, 'pk': patient.pk})

    def get_doctor(self):
        doctor = DoctorProfile.objects.get(user=self.request.user)
        return doctor

    def get_patient(self):
        patient = PatientProfile.objects.get(pk=self.kwargs['pk'])
        return patient


class UpdateOncologyStatus(DoctorRequiredMixin, UpdateView):
    template_name = 'update_oncology_status.html'
    model = OncologyStatus
    form_class = OncologyStatusForm

    def get_success_url(self):
        onco_status_pk = self.object.pk
        patient = self.get_patient()
        return reverse_lazy('view oncology status', kwargs={'onco_status': onco_status_pk, 'pk': patient.pk})

    def get_object(self, queryset=None):
        patient_id = self.kwargs['pk']
        oncology_status_id = self.kwargs['onco_status']
        obj = self.model.objects.get(patient__pk=patient_id, pk=oncology_status_id)
        return obj

    def get_patient(self):
        patient = PatientProfile.objects.get(pk=self.kwargs['pk'])
        return patient


class ViewOncologyStatus(DoctorOrSelfRequiredMixin, DetailView):
    template_name = 'view_oncology_status.html'
    model = OncologyStatus
    context_object_name = 'oncology_status'

    def get_object(self, queryset=None):
        patient_id = self.kwargs['pk']
        oncology_status_id = self.kwargs['onco_status']
        try:
            obj = self.model.objects.get(patient__pk=patient_id, pk=oncology_status_id)
        except:
            return render(self.request, '404.html', status=404)
        return obj
