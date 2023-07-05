from django.contrib.auth.mixins import UserPassesTestMixin


class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_doctor


class PatientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and not self.request.user.is_doctor
