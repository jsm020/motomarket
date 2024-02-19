from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display_links = ('id', 'full_name')
    list_display = ('id', 'full_name', 'username', 'telegram_id', 'email')
    search_fields = ('full_name', 'username', 'telegram_id', 'email')

