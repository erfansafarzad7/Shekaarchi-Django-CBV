from django.views.generic import ListView, TemplateView
from files.models import Item


class HomeView(ListView):
    """
    Home page (Show items).
    """
    template_name = 'home/home.html'
    queryset = Item.objects.all()
    context_object_name = 'items'

