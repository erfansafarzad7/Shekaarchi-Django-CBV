from django.views.generic import ListView, TemplateView
from files.models import Item
from django.db.models import Q


class HomeView(ListView):
    """
    Home page (Show items).
    """
    template_name = 'home/home.html'
    queryset = Item.objects.all()
    context_object_name = 'items'


class ItemSearchView(TemplateView):
    """
    Search between items.
    """
    model = Item
    template_name = "home/search.html"

    def get(self, request, *args, **kwargs):
        code = int(request.GET.get('code', 0))
        all_price = int(request.GET.get('all-price', 0))
        area = int(request.GET.get('area', 0))
        type = request.GET.get('type', '')
        house_type = request.GET.get('house-type', '')
        self.results = None

        # find the code
        if code:
            self.results = Item.objects.filter(Q(code__exact=code))

        # filter by allprice or area and type
        if all_price or area:
            self.results = Item.objects.filter(Q(all_price__lte=all_price) | Q(area__lte=area))
            if (all_price or area) and type:
                self.results = Item.objects.filter(Q(all_price__lte=all_price) | Q(area__lte=area), Q(type__exact=type))
            if all_price and area and type:
                self.results = Item.objects.filter(Q(all_price__lte=all_price), Q(area__lte=area), Q(type__exact=type))

        # filter by type and house type
        if type or house_type:
            self.results = Item.objects.filter(Q(type__exact=type) | Q(house_type__exact=house_type))
            if type and house_type:
                self.results = Item.objects.filter(Q(type__exact=type), Q(house_type__exact=house_type))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Add context to the template"""
        return super().get_context_data(results=self.results, **kwargs)
