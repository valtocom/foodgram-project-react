from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    fieldsets = (
    ('Общая информация', {'fields': ('first_name', 'last_name', 'email')}),
    (
        'Права доступа',
        {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        },
    ),
    ('Даты', {'fields': ('last_login')}),
)
