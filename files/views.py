from django.contrib.messages.views import SuccessMessageMixin
from .models import Item
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from files.forms import ItemCreateForm, ItemUpdateForm


class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create a new item after validation.
    user will be auto set.
    send success message and redirect to home.
    """
    model = Item
    form_class = ItemCreateForm
    template_name = 'files/create.html'
    success_message = 'Item Successfully Created'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemDetailView(DetailView):
    template_name = 'files/detail.html'
    context_object_name = 'item'

    def get_object(self, queryset=None):
        return Item.objects.get(code=self.kwargs['code'])


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'files/delete_item.html'
    context_object_name = 'item'
    success_url = reverse_lazy('home:home')

    def get_queryset(self):
        return Item.objects.get(code=self.kwargs['code'])

    def get_object(self, queryset=None):
        self.item = self.get_queryset()

    def get_context_data(self, **kwargs):
        return super().get_context_data(item=self.item, **kwargs)


class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'files/update_item.html'
    form_class = ItemUpdateForm
    context_object_name = 'item'
    success_url = reverse_lazy('home:home')

    def get_queryset(self):
        return Item.objects.get(code=self.kwargs['code'])

    def get_object(self, queryset=None):
        obj = Item.objects.get(code__exact=self.get_queryset().code)
        if not obj.user == self.request.user:
            raise None
        return obj

