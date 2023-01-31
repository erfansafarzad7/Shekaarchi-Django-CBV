from django.views.generic import ListView, TemplateView
from files.models import Item


class HomeView(ListView):
    """
    Home page (Show items).
    """
    template_name = 'home/home.html'
    queryset = Item.objects.all()
    context_object_name = 'items'


class ItemSearchView(TemplateView):
    model = Item
    template_name = "home/search.html"

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q', '')
        self.results = Item.objects.filter(code=q)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add context to the template"""
        return super().get_context_data(results=self.results, **kwargs)

