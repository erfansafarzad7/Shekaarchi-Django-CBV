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
    """
    Show items detail.
    """
    template_name = 'files/detail.html'
    context_object_name = 'item'

    def get_object(self, queryset=None):
        return Item.objects.get(code=self.kwargs['code'])


class ItemDeleteView(DeleteView):
    """
    Delete an Item.
    just item owner can do.
    """
    model = Item
    template_name = 'files/delete_item.html'

    def get_queryset(self):
        return Item.objects.get(code=self.kwargs['code'])

    def get_object(self, queryset=None):
        self.get_queryset().delete() if self.get_queryset().user == self.request.user else None


class ItemUpdateView(UpdateView):
    """
    Edit an Item.
    just item owner can do.
    """
    model = Item
    template_name = 'files/edit_item.html'
    form_class = ItemUpdateForm
    context_object_name = 'item'
    success_url = reverse_lazy('home:home')

    def get_queryset(self):
        return Item.objects.get(code=self.kwargs['code'])

    def get_object(self, queryset=None):
        obj = Item.objects.get(code__exact=self.get_queryset().code)
        return obj if obj.user == self.request.user else None

