from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Otp


@admin.action(description='Confirm avatar')
def confirm_avatar(modeladmin, request, queryset):
    queryset.update(show_avatar=True)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    actions = (confirm_avatar, )

    list_display = ('username', 'phone', 'show_avatar', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_superuser', 'show_avatar')

    # edit user
    fieldsets = (
        ('Info',
         {'fields': ('phone',  'username', 'password', 'avatar')}),

        ('Permissions',
         {'fields': ('show_avatar', 'is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    # add user
    add_fieldsets = (
        ('Add User',
            {'fields': ('username', 'phone', 'password')}),
    )

    search_fields = ('username', 'phone')
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(Otp)
class OtpAdmin(admin.ModelAdmin):
    search_fields = ('phone', )
    list_display = ('phone', 'code', 'created')
    list_filter = ('phone', 'created')


admin.site.register(User, UserAdmin)
