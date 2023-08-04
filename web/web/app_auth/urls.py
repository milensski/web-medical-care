from django.urls import path

from .views import SignInView, SignOutView, registration_step1, registration_step2, \
    doctor_profile, patient_profile, DoctorDashboard, PatientProfileDetails, PatientProfileEdit, AddOncologyStatus, \
    UpdateOncologyStatus, ViewOncologyStatus, patient_dashboard, schedule_appointment, UpdateAppointment, \
    HistoryAppointments, cancel_appointment, create_appointment_poll, ViewAppointment, reject_appointment, \
    create_treatment_plan, view_treatment_plan, update_treatment_plan, LandingPageView, index, approve_appointment, \
    DoctorProfileDetails, DoctorProfileEdit, UserProfilePictureChange

urlpatterns = [

    path('', LandingPageView.as_view(), name='landing page'),

    path('register/', registration_step1, name='registration step1'),
    path('register/step2/', registration_step2, name='registration step2'),
    path('register/step3/doctor/', doctor_profile, name='doctor profile'),
    path('register/step3/patient/', patient_profile, name='patient profile'),

    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('index/', index, name='index'),
    path('doctor/dashboard/', DoctorDashboard.as_view(), name='doctor dashboard'),
    path('schedule-appointment/', schedule_appointment, name='schedule appointment'),
    path('appointment-poll/', create_appointment_poll, name='create appointment poll'),
    path('appointment/<int:pk>/details', ViewAppointment.as_view(), name='view appointment'),
    path('appointment/<int:pk>/update', UpdateAppointment.as_view(), name='update appointment'),
    path('appointment/<int:pk>/cancel/', cancel_appointment, name='cancel appointment'),
    path('appointment/<int:pk>/reject/', reject_appointment, name='reject appointment'),
    path('appointment/<int:pk>/approve/', approve_appointment, name='approve appointment'),
    path('appointments/history/', HistoryAppointments.as_view(), name='history appointments'),
    path('create-treatment-plan/<int:patient_pk>/', create_treatment_plan, name='create treatment plan'),
    path('view-treatment-plan/<int:treatment_plan_pk>/', view_treatment_plan, name='view treatment plan'),
    path('update-treatment-plan/<int:treatment_plan_pk>/', update_treatment_plan, name='update treatment plan'),
    path('patient/dashboard/', patient_dashboard, name='patient dashboard'),
    path('patient/<int:pk>/', PatientProfileDetails.as_view(), name='patient details'),
    path('doctor/<int:pk>/', DoctorProfileDetails.as_view(), name='doctor details'),
    path('patient/<int:pk>/edit/', PatientProfileEdit.as_view(), name='patient edit'),
    path('doctor/<int:pk>/edit/', DoctorProfileEdit.as_view(), name='doctor edit'),
    path('oncology-status/<int:pk>/add/', AddOncologyStatus.as_view(), name='add oncology status'),
    path('oncology-status/<int:pk>/update/<int:onco_status>/', UpdateOncologyStatus.as_view(),
         name='update oncology status'),
    path('oncology-status/<int:pk>/view/<int:onco_status>/', ViewOncologyStatus.as_view(),
         name='view oncology status'),
    path('profile/<int:pk>/edit-photo/', UserProfilePictureChange.as_view(),
         name='profile picture change'),

]
