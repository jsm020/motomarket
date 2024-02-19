from django.contrib import admin

from .models import Product, Category, Order


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'category')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'total_amount', 'currency', 'created_time')
    list_display_links = ('id', 'user_name')
    search_fields = ('user_name', 'user_username', 'currency', 'phone_number', 'city')
    list_filter = ('created_time', 'currency')
    filter_horizontal = ('products',)
    date_hierarchy = 'created_time'
    readonly_fields = ('created_time',)
