from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from .models import User
from .forms import UserCreationForm


class LoginView(SuccessMessageMixin, LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = 'Successfully logged In!'
    next_page = reverse_lazy('home:home')


class LogoutView(LogoutView):
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
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        valid = super(RegisterView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

