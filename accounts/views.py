from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView
from files.models import Item
from .models import User
from .forms import UserCreationForm


class LoginView(SuccessMessageMixin, LoginView):
    """
    Login and send success message.
    """
    template_name = 'accounts/login.html'
    success_message = "You Have Successfully logged In!"
    next_page = reverse_lazy('home:home')


class LogoutView(LogoutView):
    """
    Logout view.
    """
    next_page = reverse_lazy('home:home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You Have Successfully logged Out!", 'warning')
        return super().dispatch(request, *args, **kwargs)


class RegisterView(SuccessMessageMixin, CreateView):
    """
    Register new user, and auto login.
    """
    template_name = 'accounts/register.html'
    form_class = UserCreationForm
    success_message = "User Successfully Created!"
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return super(RegisterView, self).form_valid(form)


class UserProfileView(ListView):
    """
    Show users profile and posts.
    Users can edit profile and delete/edit post if it's their own.
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


class UserEditProfileView(SuccessMessageMixin, UpdateView):
    """
    User can edit just own info.
    """
    model = User
    fields = ('username', 'email', 'phone_number')
    template_name = 'accounts/edit_profile.html'
    context_object_name = 'user'
    success_message = "Your Profile Successfully Edited!"
    success_url = reverse_lazy('home:home')

    def get_queryset(self):
        return User.objects.get(id=self.kwargs['pk'])

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.get_queryset().id)
        return obj if obj.id == self.request.user.id else None

