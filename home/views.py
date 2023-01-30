from django.shortcuts import render
from django.views.generic import ListView, CreateView
from files.models import Item
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from django.contrib import messages
from files.forms import ItemCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages import views as message


class HomeView(ListView):
    """
    Home page (Show items).
    """
    template_name = 'home/home.html'
    queryset = Item.objects.all()
    context_object_name = 'items'


class LoginView(message.SuccessMessageMixin, auth_view.LoginView):
    """
    Login and send success message.
    """
    success_message = 'Successfully logged In!'
    template_name = 'home/login.html'
    next_page = reverse_lazy('home:home')


class LogoutView(auth_view.LogoutView):
    """
    Logout view.
    """
    next_page = reverse_lazy('home:home')


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new item after validation.
    user will be auto set.
    send success message and redirect to home.
    """
    model = Item
    form_class = ItemCreateForm
    template_name = 'home/create.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Item Successfully Created', 'success')
        return super().form_valid(form)

