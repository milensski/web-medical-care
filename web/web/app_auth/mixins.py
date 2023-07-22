from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import View

from web.app_auth.models import DoctorProfile, PatientProfile


class DoctorRequiredMixin(View):
    def test_func(self):
        return

    def dispatch(self, request, *args, **kwargs):
        exist = DoctorProfile.objects.filter(user=self.request.user).exists()
        if self.request.user.is_authenticated and exist:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')


class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_doctor


class LoggedUserRedirectMixin(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            try:
                if self.request.user.groups.filter(name='Doctors').exists():
                    return redirect('doctor dashboard')
                elif self.request.user.groups.filter(name='Patients').exists():
                    return redirect('patient dashboard')
            except (DoctorProfile.DoesNotExist, PatientProfile.DoesNotExist):
                # Profile does not exist
                pass
        return super().dispatch(request, *args, **kwargs)
