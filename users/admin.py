from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Кастомная админка для пользователя"""

    # Поля, отображаемые в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'patronymic', 'role', 'is_staff')

    # Поля для фильтрации
    list_filter = ('role', 'is_staff', 'is_active')

    # Поля для поиска
    search_fields = ('username', 'email', 'first_name', 'last_name', 'patronymic')

    # Сортировка по умолчанию
    ordering = ('username',)

    # Настройка формы редактирования пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'patronymic', 'email')}),
        ('Права доступа', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Настройка формы создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'patronymic', 'role', 'password1', 'password2'),
        }),
    )


# Перерегистрируем модель с новым админ-классом
admin.site.register(CustomUser, CustomUserAdmin)