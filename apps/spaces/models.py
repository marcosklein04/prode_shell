"""Modelos de salas/espacios para torneos privados."""

import secrets
import string

from django.conf import settings
from django.db import models

from core.mixins import TimestampMixin


def generar_codigo(longitud=8):
    """Genera un código alfanumérico único para unirse a la sala."""
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))


class Sala(TimestampMixin):
    """Sala/espacio donde un grupo de usuarios compite con ranking propio."""

    nombre = models.CharField('Nombre', max_length=200)
    descripcion = models.TextField('Descripción', blank=True)
    codigo = models.CharField(
        'Código de invitación',
        max_length=20,
        unique=True,
        default=generar_codigo,
        db_index=True,
    )
    creador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='salas_creadas',
        verbose_name='Creador',
    )
    es_publica = models.BooleanField('Es pública', default=False)
    max_miembros = models.PositiveIntegerField('Máx. miembros', default=100)
    activa = models.BooleanField('Activa', default=True)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
        ordering = ['-created_at']

    def __str__(self):
        return self.nombre

    @property
    def cantidad_miembros(self):
        return self.miembros.count()


class MiembroSala(TimestampMixin):
    """Relación entre un usuario y una sala."""

    class Rol(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        MIEMBRO = 'miembro', 'Miembro'

    sala = models.ForeignKey(
        Sala,
        on_delete=models.CASCADE,
        related_name='miembros',
        verbose_name='Sala',
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='membresias',
        verbose_name='Usuario',
    )
    rol = models.CharField(
        'Rol',
        max_length=10,
        choices=Rol.choices,
        default=Rol.MIEMBRO,
    )

    class Meta:
        verbose_name = 'Miembro de sala'
        verbose_name_plural = 'Miembros de sala'
        unique_together = [('sala', 'usuario')]

    def __str__(self):
        return f'{self.usuario.email} en {self.sala.nombre}'
