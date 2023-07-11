from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect


class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_doctor


class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_doctor


class LoggedUserRedirectMixin(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)
