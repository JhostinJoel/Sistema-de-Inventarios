from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.inventory.models import Product

class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Nombre Completo'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Teléfono'))
    address = models.TextField(blank=True, verbose_name=_('Dirección'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Cliente')
        verbose_name_plural = _('Clientes')

    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Nombre/Empresa'))
    contact_name = models.CharField(max_length=200, blank=True, verbose_name=_('Contacto'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Teléfono'))
    address = models.TextField(blank=True, verbose_name=_('Dirección'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Proveedor')
        verbose_name_plural = _('Proveedores')

    def __str__(self):
        return self.name

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name=_('Cliente'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('Vendedor'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_('Total'))
    
    class Meta:
        verbose_name = _('Venta')
        verbose_name_plural = _('Ventas')

    def __str__(self):
        return f"Venta #{self.id} - {self.client.name}"

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Producto'))
    quantity = models.IntegerField(verbose_name=_('Cantidad'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Precio Unitario'))
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Subtotal'))

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Detalle de Venta')
        verbose_name_plural = _('Detalles de Venta')

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name=_('Proveedor'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name=_('Comprador'))
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Fecha'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name=_('Total'))
    
    class Meta:
        verbose_name = _('Compra')
        verbose_name_plural = _('Compras')

    def __str__(self):
        return f"Compra #{self.id} - {self.supplier.name}"

class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, related_name='details', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Producto'))
    quantity = models.IntegerField(verbose_name=_('Cantidad'))
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Costo Unitario'))
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('Subtotal'))

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.cost
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Detalle de Compra')
        verbose_name_plural = _('Detalles de Compra')
