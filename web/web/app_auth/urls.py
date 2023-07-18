from django.urls import path

from .views import SignInView, SignOutView, index, registration_step1, registration_step2, \
    doctor_profile, patient_profile, DoctorDashboard, PatientProfileDetails, PatientProfileEdit, AddOncologyStatus, \
    UpdateOncologyStatus, ViewOncologyStatus, patient_dashboard, schedule_appointment, UpdateAppointment, \
    HistoryAppointments, cancel_appointment, create_appointment_poll

urlpatterns = [
    path('register/', registration_step1, name='registration step1'),
    path('register/step2/', registration_step2, name='registration step2'),
    path('register/step3/doctor/', doctor_profile, name='doctor profile'),
    path('register/step3/patient/', patient_profile, name='patient profile'),

    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('', index, name='index'),
    path('dashboard/', DoctorDashboard.as_view(), name='doctor dashboard'),
    path('schedule-appointment/', schedule_appointment, name='schedule appointment'),
    path('appointment-poll/', create_appointment_poll, name='create appointment poll'),
    path('appointment/<int:pk>/', UpdateAppointment.as_view(), name='view appointment'),
    path('appointment/<int:pk>/cancel/', cancel_appointment, name='cancel appointment'),
    path('appointments/history/', HistoryAppointments.as_view(), name='history appointments'),
    path('patient/dashboard/', patient_dashboard, name='patient dashboard'),
    path('patient/<int:pk>/', PatientProfileDetails.as_view(), name='patient details'),
    path('patient/<int:pk>/edit/', PatientProfileEdit.as_view(), name='patient edit'),
    path('oncology-status/<int:pk>/add/', AddOncologyStatus.as_view(), name='add oncology status'),
    path('oncology-status/<int:pk>/update/<int:onco_status>/', UpdateOncologyStatus.as_view(),
         name='update oncology status'),
    path('oncology-status/<int:pk>/view/<int:onco_status>/', ViewOncologyStatus.as_view(),
         name='view oncology status'),

]
