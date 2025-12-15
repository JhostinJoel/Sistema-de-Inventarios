from django.contrib import admin
from .models import Category, Product, Warehouse, InventoryMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'price', 'stock', 'min_stock')
    list_filter = ('category',)
    search_fields = ('name', 'code')

@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'movement_type', 'quantity', 'created_at', 'user')
    list_filter = ('movement_type', 'warehouse')
    search_fields = ('product__name',)
