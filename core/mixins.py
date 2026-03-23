"""Mixins reutilizables para modelos."""

from django.db import models


class TimestampMixin(models.Model):
    """Mixin que agrega campos de auditoría created_at y updated_at."""

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    class Meta:
        abstract = True
