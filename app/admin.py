from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from app.models import Client
from app.models import UserToken
from app.models import User as CustomUser

ADMIN = 'Адмін'
WORKER = 'Робітник'


class UserFilter(admin.SimpleListFilter):
    title = _('Фільтрація по ролі')
    parameter_name = 'Фільтрація по ролі'

    def lookups(self, request, model_admin):
        return (
            (ADMIN, _('Адмін')),
            (WORKER, _('Робітник')),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value is None:
            return queryset.all()

        is_staff = value == ADMIN and True or False

        return queryset.filter(is_staff=is_staff)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username')

    list_display_links = ('id', 'username')

    list_filter = UserFilter,

    fieldsets = (
        (_('Головні дані'), {
            'fields': ('username', 'password'),
            'classes': ('collapse',)
        }),
        (_('Додаткові дані'), {
            'fields': ('first_name', 'last_name', 'email'),
            'classes': ('collapse',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")
    list_display_links = ("id", "name", "email")
    search_fields = ("name", "email")


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ("id",)
    list_display_links = ("id",)

    has_change_permission = lambda self, request, obj=None: False
    has_delete_permission = lambda self, request, obj=None: False
