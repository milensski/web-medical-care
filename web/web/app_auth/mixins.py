from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import View

from web.app_auth.models import DoctorProfile


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
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
