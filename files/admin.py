from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Item, Image


class AreaFilter(SimpleListFilter):
    """
    Custom area admin filter.
    """
    title = 'Area'
    parameter_name = 'Area Filter'

    def lookups(self, request, model_admin):
        return (
            (100, '100'),
            (300, '300'),
            (500, '500'),
            (1000, '1000'),
            (3000, '3000'),
            (5000, '5000'),
            (10000, '10000'),
            (30000, '30000'),
            (50000, '50000'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(area__lte=self.value())


class AllPriceFilter(admin.SimpleListFilter):
    """
    Custom all price admin filter.
    """
    title = 'All Price'
    parameter_name = 'All Price'

    def lookups(self, request, model_admin):
        return (
            (500000000, '500/000/000'),
            (1000000000, '1/000/000/000'),
            (2000000000, '2/000/000/000'),
            (3000000000, '3/000/000/000'),
            (4000000000, '4/000/000/000'),
            (5000000000, '5/000/000/000'),
            (10000000000, '10/000/000/000'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(all_price__lte=self.value())


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ('code', )
    list_display = ('code', 'type', 'area', 'foundation', 'all_price', 'created')
    list_filter = (AreaFilter, AllPriceFilter,
                   'type', 'house_type',  'deed', 'exchange', 'land_type', 'rice_field_type',  'inside_plan', 'created')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ('code', )
    list_display = ('code', 'uploaded')
    list_filter = ('uploaded', )

