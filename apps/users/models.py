from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrador')
        SELLER = 'SELLER', _('Vendedor')
        WAREHOUSE = 'WAREHOUSE', _('Almacenista')

    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.SELLER,
        verbose_name=_('Rol')
    )
    
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Teléfono'))
    
    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class AuditLog(models.Model):
    class Action(models.TextChoices):
        CREATE = 'CREATE', _('Crear')
        UPDATE = 'UPDATE', _('Actualizar')
        DELETE = 'DELETE', _('Eliminar')
        LOGIN = 'LOGIN', _('Inicio de sesión')
        LOGOUT = 'LOGOUT', _('Cierre de sesión')
        VIEW = 'VIEW', _('Ver')

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Usuario'))
    action = models.CharField(max_length=20, choices=Action.choices, verbose_name=_('Acción'))
    model_name = models.CharField(max_length=100, blank=True, verbose_name=_('Modelo'))
    object_id = models.CharField(max_length=100, blank=True, verbose_name=_('ID del Objeto'))
    description = models.TextField(blank=True, verbose_name=_('Descripción'))
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name=_('IP'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Registro de Auditoría')
        verbose_name_plural = _('Registros de Auditoría')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.model_name}"
