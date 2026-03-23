"""Modelo de pronósticos."""

from django.conf import settings
from django.db import models

from apps.matches.models import Partido
from core.mixins import TimestampMixin


class Pronostico(TimestampMixin):
    """Pronóstico de un usuario para un partido."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pronosticos',
        verbose_name='Usuario',
    )
    partido = models.ForeignKey(
        Partido,
        on_delete=models.CASCADE,
        related_name='pronosticos',
        verbose_name='Partido',
    )
    goles_local = models.PositiveIntegerField('Goles local')
    goles_visitante = models.PositiveIntegerField('Goles visitante')
    puntos = models.IntegerField('Puntos obtenidos', null=True, blank=True)

    class Meta:
        verbose_name = 'Pronóstico'
        verbose_name_plural = 'Pronósticos'
        unique_together = [('usuario', 'partido')]
        ordering = ['partido__fecha_hora']
        indexes = [
            models.Index(fields=['usuario', 'partido'], name='idx_usuario_partido'),
        ]

    def __str__(self):
        return (
            f'{self.usuario.email} - {self.partido}: '
            f'{self.goles_local}-{self.goles_visitante}'
        )
