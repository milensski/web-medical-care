from django.urls import path

from .views import SignInView, SignOutView, index, registration_step1, registration_step2, \
    doctor_profile, patient_profile

urlpatterns = [
    path('register/', registration_step1, name='registration step1'),
    path('register/step2/', registration_step2, name='registration step2'),
    path('register/step3/doctor/', doctor_profile, name='doctor profile'),
    path('register/step3/patient/', patient_profile, name='patient profile'),

    path('login/', SignInView.as_view(), name='login'),
    path('logout/', SignOutView.as_view(), name='logout'),
    path('', index, name='index'),

]
