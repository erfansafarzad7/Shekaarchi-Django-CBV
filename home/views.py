from django.shortcuts import render
from django.views.generic.list import ListView
from files.models import Item


class HomeView(ListView):
    template_name = 'home/home.html'
    # model = Item
    # queryset = Car.objects.filter(year__gte=2000)
    context_object_name = 'items'
    # ordering = 'year'

    def get_queryset(self):
        return Item.objects.all()

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['username'] = 'jack'
    #     return context

