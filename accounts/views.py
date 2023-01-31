from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from .models import User
from .forms import UserCreationForm


class LoginView(SuccessMessageMixin, auth_view.LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = 'Successfully logged In!'
    next_page = reverse_lazy('home:home')


class LogoutView(auth_view.LogoutView):
    """
    Logout view.
    """
    next_page = reverse_lazy('home:home')


class RegisterView(SuccessMessageMixin, CreateView):
    """
    Register new user.
    """
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_message = 'User Successfully Created!'
    success_url = reverse_lazy('accounts:login')

