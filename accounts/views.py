from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, ListView
from files.models import Item
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


class UserProfileView(ListView):
    """
    Show users profile and posts.
    Users can edit profile and delete/edit their post if it's their own.
    """
    template_name = 'accounts/user_profile.html'
    model = Item
    context_object_name = 'items'

    def get_queryset(self):
        return Item.objects.filter(user__exact=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        self.items_user = User.objects.get(id=kwargs['pk'])
        return super().get(request, *args, **kwargs) if self.items_user == request.user else None

    def get_context_data(self, **kwargs):
        return super().get_context_data(items_user=self.items_user.id, **kwargs)

