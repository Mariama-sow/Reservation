from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import CreateView
from django.db import transaction

class CustomUserLogin(LoginView):
    authentication_form = CustomUserLoginForm
    template_name = 'users/login.html'
    # redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, "Connexion réussie!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')  # Rediriger vers la page d'accueil après connexion


class CustomLogoutView(LogoutView):
    # next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Votre compte a été déconnecté.")
        return super().dispatch(request, *args, **kwargs)

class CustomUserCreation(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/creation.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        with transaction.atomic():
            form.save()
        messages.success(self.request, "Votre compte a été créé avec succès.")
        return redirect(self.success_url)
