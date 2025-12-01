from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Notification(models.Model):
    class Type(models.TextChoices):
        INFO = 'INFO', _('Información')
        WARNING = 'WARNING', _('Advertencia')
        SUCCESS = 'SUCCESS', _('Éxito')
        ERROR = 'ERROR', _('Error')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('Usuario'))
    title = models.CharField(max_length=200, verbose_name=_('Título'))
    message = models.TextField(verbose_name=_('Mensaje'))
    notification_type = models.CharField(max_length=10, choices=Type.choices, default=Type.INFO, verbose_name=_('Tipo'))
    is_read = models.BooleanField(default=False, verbose_name=_('Leída'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Notificación')
        verbose_name_plural = _('Notificaciones')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"
