from django.views.generic import ListView
from files.models import Item, Image
from django.db.models import Q
from django.contrib import messages


class HomeView(ListView):
    """
    Home page (Show items).
    """
    template_name = 'home/home.html'
    queryset = Item.objects.all().filter(publish=True, public=True)
    context_object_name = 'items'
    ordering = ('-updated', )
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        """
        Add images after edit item.
        """
        if 'add_image' in request.session:
            session = request.session['add_image']
            item = Item.objects.get(code__exact=session['code'])
            image = Image.objects.filter(code__exact=session['code'])
            for img in image:
                item.images.add(img)
            del request.session['add_image']
        return super(HomeView, self).get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        i=0
        for item in self.get_queryset():
            i+=1
        context["allItems"] = i
        return context


class ItemSearchView(ListView):
    """
    Search between items.
    """
    model = Item
    template_name = 'home/search.html'

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "جستوجو انجام شد !", 'info')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # find item by code
        code = request.GET.get('code', '')
        search_in_all = False if request.GET.get('search_in', '') == 'profile' else True
        self.results = Item.objects.all().filter(publish=True, public=True)

        if code > '0' and code.isnumeric():
            if search_in_all:
                self.results = Item.objects.filter(Q(code__exact=code), Q(public=True), Q(publish=True))
            else:
                self.results = Item.objects.filter(Q(code__exact=code), Q(user__exact=self.request.user))

        # filter items by query parameters
        for qp in self.request.GET.items():

            # qp[0] is query parameter(field)
            # qp[1] is query parameters value
            if qp[0] == 'area' and qp[1]:
                self.results = self.results.filter(area__lte=int(qp[1]) or 0).order_by('area')
            if qp[0] == 'all_price' and qp[1]:
                self.results = self.results.filter(all_price__lte=int(qp[1]) or 0)
            if qp[0] == 'all_rent_price' and qp[1]:
                self.results = self.results.filter(subject='rent').filter(all_rent_price__lte=int(qp[1]) or 0)
            if qp[0] == 'rent' and qp[1]:
                self.results = self.results.filter(subject='rent').filter(rent__lte=int(qp[1]) or 0)

            if qp[0] == 'subject' and qp[1]:
                self.results = self.results.filter(subject__exact=qp[1])

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

            if qp[0] == 'state' and qp[1]:
                self.results = self.results.filter(Q(state__contains=qp[1]))

            if qp[0] == 'city' and qp[1]:
                self.results = self.results.filter(Q(city__contains=qp[1]))

            if qp[0] == 'village' and qp[1]:
                self.results = self.results.filter(Q(village__contains=qp[1]))

            if qp[0] == 'search_in' and qp[1]:
                if qp[1] == 'profile':
                    self.results = self.results.filter(user__exact=self.request.user)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.results:
            context['results'] = self.results.order_by('-updated')
        else:
            context['results'] = self.results

        i=0
        for item in self.results:
            i+=1
        context["allItems"] = i
        return context
