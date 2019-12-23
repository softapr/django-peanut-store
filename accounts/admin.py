from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin as _GroupAdmin
from dapricot.store.accounts.models import User, Group
from django.utils.translation import gettext, gettext_lazy as _

from dapricot.store.core.admin import site

@admin.register(Group, site=site)
class GroupAdmin(_GroupAdmin):
    pass

@admin.register(User, site=site)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login', 'date_joined', 'email', 'first_name', 'last_name', 'password')

    def get_queryset(self, request):
        queryset = super(UserAdmin, self).get_queryset(request)
        
        return queryset.filter(is_staff=True)