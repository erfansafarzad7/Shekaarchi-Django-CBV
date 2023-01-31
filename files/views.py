from django.shortcuts import render
from django.views.generic import DetailView
from .models import Item
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from files.forms import ItemCreateForm


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new item after validation.
    user will be auto set.
    send success message and redirect to home.
    """
    model = Item
    form_class = ItemCreateForm
    template_name = 'files/create.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Item Successfully Created', 'success')
        return super().form_valid(form)


class ItemDetailView(DetailView):
    template_name = 'files/detail.html'
    context_object_name = 'item'

    def get_object(self, queryset=None):
        return Item.objects.get(code=self.kwargs['code'])

