from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'phone_number', 'is_admin', 'is_superuser')
    list_filter = ('is_admin', 'is_superuser')

    # edit user
    fieldsets = (
        ('Info',
         {'fields': ('phone_number', 'email', 'username', 'password')}),

        ('Permissions',
         {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    # add user
    add_fieldsets = (
        ('Add User',
            {'fields': ('username', 'phone_number', 'email', 'password1', 'password2')}),
    )

    search_fields = ('email', 'username', 'phone_number')
    ordering = ('username', )
    filter_horizontal = ('groups', 'user_permissions')


admin.site.register(User, UserAdmin)

