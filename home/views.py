from django.shortcuts import render
from django.views.generic.list import ListView
from files.models import Item
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy


class HomeView(ListView):
    template_name = 'home/home.html'
    queryset = Item.objects.all()
    context_object_name = 'items'


class LoginView(auth_view.LoginView):
    template_name = 'home/login.html'
    next_page = reverse_lazy('home:home')


class LogoutView(auth_view.LogoutView):
    next_page = reverse_lazy('home:home')

