from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, View

from .forms import SignUpForm, SignInForm
from .models import CustomUser


class SignUpView(CreateView):
    model = CustomUser
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        # Exclude the superuser from being set as a patient
        if not self.request.user.is_superuser:
            form.instance.is_doctor = False

        result = super().form_valid(form)

        login(self.request, self.object)

        return result


class SignInView(LoginView):
    form_class = SignInForm
    template_name = 'signin.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.get_user()

        print(login(self.request, user))

        return super().form_valid(form)


class SignOutView(LogoutView):
    pass


@login_required
def index(request):
    return render(request, 'index.html')
