from django.views.generic import ListView, TemplateView
from files.models import Item
from django.db.models import Q
from django.contrib import messages


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
    template_name = 'home/search.html'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "I Fund This Results!", 'info')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        code = int(request.GET.get('code', 0))
        all_price = int(request.GET.get('all-price', 0))
        area = int(request.GET.get('area', 0))
        type = request.GET.get('type', '')
        house_type = request.GET.get('house-type', '')
        land_type = request.GET.get('land-type', '')
        rice_field_type = request.GET.get('rice-field-type', '')
        search_in = request.GET.get('search-in', '')
        self.results = None

        # find item by code
        if code:
            self.results = Item.objects.filter(Q(code__exact=code))

        # filter by all price or area and type if entered
        if all_price or area:
            self.results = Item.objects.filter(
                Q(all_price__lte=all_price) | Q(area__lte=area))

            if (all_price or area) and type:
                self.results = Item.objects.filter(
                    Q(all_price__lte=all_price) | Q(area__lte=area),
                    Q(type__exact=type))

            if all_price and area and type:
                self.results = Item.objects.filter(
                    Q(all_price__lte=all_price),
                    Q(area__lte=area),
                    Q(type__exact=type))

        # filter by type and house/land type and rice field type
        if type or house_type or land_type or rice_field_type:
            self.results = Item.objects.filter(
                Q(type__exact=type) | Q(house_type__exact=house_type) | Q(land_type__exact=land_type))

            if type and (house_type or land_type):
                self.results = Item.objects.filter(
                    Q(type__exact=type),
                    Q(house_type__exact=house_type) | Q(land_type__exact=land_type))

                if land_type == 'rice_field' and rice_field_type:
                    self.results = Item.objects.filter(
                        Q(land_type__exact='rice_field'),
                        Q(rice_field_type__exact=rice_field_type))

        # search in user files
        if search_in == 'my-files':
            self.results = self.results.filter(user=self.request.user)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add context to the template
        """
        return super().get_context_data(results=self.results, **kwargs)
