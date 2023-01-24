from django.shortcuts import render
from django.views.generic import DetailView
from .models import Item


class ItemDetailView(DetailView):
    template_name = 'home/detail.html'
    # model = Car
    context_object_name = 'item'
    # slug_field = 'name'
    # slug_url_kwarg = 'my_slug'
    # pk_url_kwarg = 'my_pk'
    # queryset = Car.objects.filter(year__gte=2000)

    # def get_queryset(self):
    #     if self.request.user.is_authenticated:
    #         return Car.objects.filter(name=self.kwargs['pk'])
    #     else:
    #         return Car.objrcts.none()

    def get_object(self, queryset=None):
        return Item.objects.get(code=self.kwargs['code'])

