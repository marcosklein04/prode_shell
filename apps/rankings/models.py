"""Modelos de reglas de puntaje."""

from django.db import models

from apps.tournaments.models import Torneo
from core.mixins import TimestampMixin


class ReglaPuntaje(TimestampMixin):
    """Regla configurable de puntaje para el prode."""

    class TipoRegla(models.TextChoices):
        RESULTADO_EXACTO = 'resultado_exacto', 'Resultado exacto'
        ACIERTO_GANADOR = 'acierto_ganador', 'Acertar ganador/empate'

    torneo = models.ForeignKey(
        Torneo,
        on_delete=models.CASCADE,
        related_name='reglas_puntaje',
        verbose_name='Torneo',
    )
    tipo = models.CharField(
        'Tipo de regla',
        max_length=30,
        choices=TipoRegla.choices,
    )
    puntos = models.IntegerField('Puntos')
    descripcion = models.CharField('Descripción', max_length=200, blank=True)

    class Meta:
        verbose_name = 'Regla de puntaje'
        verbose_name_plural = 'Reglas de puntaje'
        unique_together = [('torneo', 'tipo')]

    def __str__(self):
        return f'{self.get_tipo_display()}: {self.puntos} pts'
