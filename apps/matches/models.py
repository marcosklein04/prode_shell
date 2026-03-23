"""Modelo de partidos."""

from django.db import models

from apps.tournaments.models import Equipo, Fase
from core.mixins import TimestampMixin


class Partido(TimestampMixin):
    """Representa un partido del mundial."""

    class Estado(models.TextChoices):
        PROGRAMADO = 'programado', 'Programado'
        EN_JUEGO = 'en_juego', 'En juego'
        FINALIZADO = 'finalizado', 'Finalizado'
        SUSPENDIDO = 'suspendido', 'Suspendido'
        CANCELADO = 'cancelado', 'Cancelado'
        POSTERGADO = 'postergado', 'Postergado'

    fase = models.ForeignKey(
        Fase,
        on_delete=models.CASCADE,
        related_name='partidos',
        verbose_name='Fase',
    )
    equipo_local = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='partidos_local',
        verbose_name='Equipo local',
    )
    equipo_visitante = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name='partidos_visitante',
        verbose_name='Equipo visitante',
    )
    fecha_hora = models.DateTimeField('Fecha y hora', db_index=True)
    estado = models.CharField(
        'Estado',
        max_length=20,
        choices=Estado.choices,
        default=Estado.PROGRAMADO,
        db_index=True,
    )
    goles_local = models.IntegerField('Goles local', null=True, blank=True)
    goles_visitante = models.IntegerField('Goles visitante', null=True, blank=True)
    api_externa_id = models.IntegerField(
        'ID en API externa',
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        ordering = ['fecha_hora']
        indexes = [
            models.Index(fields=['fecha_hora', 'estado'], name='idx_fecha_estado'),
        ]

    def __str__(self):
        return f'{self.equipo_local} vs {self.equipo_visitante} ({self.get_estado_display()})'

    @property
    def esta_abierto_para_pronosticos(self):
        """Un partido acepta pronósticos si está programado."""
        return self.estado == self.Estado.PROGRAMADO

    @property
    def resultado_texto(self):
        if self.goles_local is not None and self.goles_visitante is not None:
            return f'{self.goles_local} - {self.goles_visitante}'
        return 'Sin resultado'
