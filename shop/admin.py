from django.contrib import admin
from .models import Category, Product, CartItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'price', 'stock', 'featured', 'created_at']
    list_filter = ['category', 'brand', 'featured', 'created_at']
    list_editable = ['price', 'stock', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'brand', 'description']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'quantity', 'session_key', 'added_at']
    list_filter = ['added_at']
