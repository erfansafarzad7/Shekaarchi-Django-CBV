from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from .models import Item, Image
import datetime


class AreaFilter(SimpleListFilter):
    """
    Custom area admin filter.
    """
    title = 'متراژ'
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
    title = 'قیمت کل'
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


class AllRentPriceFilter(admin.SimpleListFilter):
    """
    Custom all rent price admin filter.
    """
    title = 'ودیعه'
    parameter_name = 'All Rent Price'

    def lookups(self, request, model_admin):
        return (
            (100000000, '100/000/000'),
            (200000000, '200/000/000'),
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
            return queryset.filter(all_rent_price__lte=self.value()).filter(subject='rent')


class RentFilter(admin.SimpleListFilter):
    """
    Custom rent admin filter.
    """
    title = 'کرایه'
    parameter_name = 'Rent'

    def lookups(self, request, model_admin):
        return (
            (500000000, '500/000/000'),
            (1000000000, '1/000/000/000'),
            (2000000000, '2/000/000/000'),
            (3000000000, '3/000/000/000'),
            (4000000000, '4/000/000/000'),
            (5000000000, '5/000/000/000'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rent__lte=self.value()).filter(subject='rent')

# mark selected items as publish
@admin.action(description='Mark as published')
def make_published(modeladmin, request, queryset):
    queryset.update(publish=True)

# mark selected items as unpublish
@admin.action(description='Mark as published')
def make_published(modeladmin, request, queryset):
    queryset.update(publish=False)

# set selected items time to now
@admin.action(description='Set time now')
def set_time_now(modeladmin, request, queryset):
    queryset.update(updated=datetime.datetime.now())


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    search_fields = ('code', )
    actions = (make_published, set_time_now)
    list_display = ('code',
                    'type',
                    'subject',
                    'area',
                    'foundation',
                    'all_price',
                    'publish',
                    'public',
                    'city',
                    'updated')

    list_filter = (AreaFilter,
                   AllPriceFilter,
                   AllRentPriceFilter,
                   RentFilter,
                   'subject',
                   'publish',
                   'public',
                   'type',
                   'house_type',
                   'documents',
                   'exchange',
                   'land_type',
                   'rice_field_type',
                   'inside_plan',
                   'city',
                   'updated')


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    search_fields = ('code', )
    list_display = ('code', 'uploaded')
    list_filter = ('uploaded', )

