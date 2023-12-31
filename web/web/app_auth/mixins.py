from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views import View

from web.app_auth.models import DoctorProfile, PatientProfile


class DoctorRequiredMixin(LoginRequiredMixin):

    def dispatch(self, request, *args, **kwargs):
        try:
            exist = DoctorProfile.objects.filter(user=request.user).exists()
        except TypeError:
            return redirect('index')
        if request.user.is_authenticated and exist:
            return super().dispatch(request, *args, **kwargs)
        return redirect('index')


class DoctorOrSelfRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.pk != kwargs['pk'] and \
                     request.user.groups.all()[0].name != 'Doctors':
                return redirect('index')
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('landing page')


class SelfRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.pk == kwargs['pk']:
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class LoggedUserRedirectMixin(LoginView):

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser:
                return redirect('index')
            try:
                if self.request.user.groups.filter(name='Doctors').exists():
                    return redirect('doctor dashboard')
                elif self.request.user.groups.filter(name='Patients').exists():
                    return redirect('patient dashboard')
                else:
                    return redirect('registration step2')

            except (DoctorProfile.DoesNotExist, PatientProfile.DoesNotExist):
                # Profile does not exist
                pass
        return super().dispatch(request, *args, **kwargs)
