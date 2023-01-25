from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Item


class AreaFilter(SimpleListFilter):
    title = 'Area'
    parameter_name = 'Area Filter'

    def lookups(self, request, model_admin):
        return [(i.area, i.area) for i in model_admin.model.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(area__lte=self.value())


class AllPriceFilter(admin.SimpleListFilter):

    title = 'All Price'
    parameter_name = 'All Price'

    def lookups(self, request, model_admin):
        return [(i.all_price, i.all_price) for i in model_admin.model.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(all_price__lte=self.value())


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ('code', )
    list_display = ('code', 'area', 'foundation', 'all_price', 'created')
    list_filter = (AreaFilter, AllPriceFilter, 'deed', 'exchange', 'created')

