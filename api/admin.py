from django.contrib import admin
from .models import Furniture, Inventory

@admin.register(Furniture)
class FurnitureAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    search_fields = ('name', 'category')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('furniture', 'quantity')
