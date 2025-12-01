from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Nombre'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Categoría')
        verbose_name_plural = _('Categorías')

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Nombre'))
    location = models.CharField(max_length=200, blank=True, verbose_name=_('Ubicación'))
    
    class Meta:
        verbose_name = _('Almacén')
        verbose_name_plural = _('Almacenes')

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name=_('Código'))
    name = models.CharField(max_length=200, verbose_name=_('Nombre'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name=_('Categoría'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Precio de Venta'))
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Costo'))
    stock = models.IntegerField(default=0, verbose_name=_('Stock Actual'))
    min_stock = models.IntegerField(default=5, verbose_name=_('Stock Mínimo'))
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name=_('Imagen'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Producto')
        verbose_name_plural = _('Productos')

    def __str__(self):
        return f"{self.name} ({self.code})"

class InventoryMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = 'IN', _('Entrada')
        OUT = 'OUT', _('Salida')
        ADJUSTMENT = 'ADJ', _('Ajuste')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Producto'))
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, verbose_name=_('Almacén'))
    quantity = models.IntegerField(verbose_name=_('Cantidad'))
    movement_type = models.CharField(max_length=3, choices=MovementType.choices, verbose_name=_('Tipo de Movimiento'))
    reason = models.CharField(max_length=255, blank=True, verbose_name=_('Razón'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name=_('Usuario'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Movimiento de Inventario')
        verbose_name_plural = _('Movimientos de Inventario')

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"
