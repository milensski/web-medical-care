from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from .forms import SignUpForm, SignInForm, SignOutForm
from .models import CustomUser


class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Exclude the superuser from being set as a patient
        if not self.request.user.is_superuser:
            form.instance.is_doctor = False

        # Perform any additional logic or customization here

        # Log in the user after successful registration
        user = form.save()
        login(self.request, user)

        return super().form_valid(form)


class SignInView(FormView):
    form_class = SignInForm
    template_name = 'signin.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class SignOutView(FormView):
    form_class = SignOutForm
    template_name = 'signout.html'
    success_url = reverse_lazy('home')  # Redirect to the home page or any desired URL

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)
