from django.views.generic import ListView
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
    ordering = ('-created', )
    paginate_by = 10


class ItemSearchView(ListView):
    """
    Search between items.
    """
    model = Item
    template_name = 'home/search.html'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "I Fund This Results!", 'info')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # find item by code
        code = int(request.GET.get('code', 0))
        self.results = Item.objects.all()

        if code:
            self.results = self.results.filter(Q(code__exact=code))

        # filter items by query parameters
        for qp in self.request.GET.items():

            # qp[0] is field
            # qp[1] is fields value
            if qp[0] == 'area' and qp[1] != '0':
                self.results = self.results.filter(area__lte=int(qp[1]))
            if qp[0] == 'all_price' and qp[1] != '0':
                self.results = self.results.filter(all_price__lte=int(qp[1]))

            if qp[0] == 'type' and qp[1]:
                self.results = self.results.filter(type__exact=qp[1])

            if qp[0] == 'house_type' and qp[1]:
                self.results = self.results.filter(house_type__exact=qp[1])

            if qp[0] == 'documents' and qp[1]:
                self.results = self.results.filter(documents__exact=qp[1])

            if qp[0] == 'land_type' and qp[1]:
                self.results = self.results.filter(land_type__exact=qp[1])

            if qp[0] == 'rice_field_type' and qp[1]:
                self.results = self.results.filter(rice_field_type__exact=qp[1])

            if qp[0] == 'search_in' and qp[1]:
                if qp[1] == 'my_files':
                    self.results = self.results.filter(user__exact=self.request.user)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add context to the template
        """
        return super().get_context_data(results=self.results.order_by('-created'), **kwargs)
