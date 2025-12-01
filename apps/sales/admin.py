from django.contrib import admin
from .models import Client, Supplier, Sale, SaleDetail, Purchase, PurchaseDetail

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')
    search_fields = ('name', 'email')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_name', 'email')
    search_fields = ('name',)

class SaleDetailInline(admin.TabularInline):
    model = SaleDetail
    extra = 1

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'date', 'total', 'user')
    inlines = [SaleDetailInline]
    list_filter = ('date',)

class PurchaseDetailInline(admin.TabularInline):
    model = PurchaseDetail
    extra = 1

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'supplier', 'date', 'total', 'user')
    inlines = [PurchaseDetailInline]
    list_filter = ('date',)
