"""Modelos de torneo, fases y equipos."""

from django.db import models

from core.mixins import TimestampMixin


class Torneo(TimestampMixin):
    """Representa un torneo (ej: Mundial 2026)."""

    nombre = models.CharField('Nombre', max_length=200)
    temporada = models.IntegerField('Temporada/Año')
    api_externa_id = models.IntegerField(
        'ID en API externa',
        unique=True,
        null=True,
        blank=True,
    )
    activo = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Torneo'
        verbose_name_plural = 'Torneos'
        ordering = ['-temporada']

    def __str__(self):
        return f'{self.nombre} {self.temporada}'


class Fase(TimestampMixin):
    """Fase del torneo (Grupos, Octavos, Cuartos, etc.)."""

    torneo = models.ForeignKey(
        Torneo,
        on_delete=models.CASCADE,
        related_name='fases',
        verbose_name='Torneo',
    )
    nombre = models.CharField('Nombre', max_length=100)
    orden = models.IntegerField('Orden', default=0)

    class Meta:
        verbose_name = 'Fase'
        verbose_name_plural = 'Fases'
        ordering = ['orden']
        unique_together = [('torneo', 'nombre')]

    def __str__(self):
        return f'{self.torneo} - {self.nombre}'


class Equipo(TimestampMixin):
    """Equipo participante del torneo."""

    nombre = models.CharField('Nombre', max_length=200)
    codigo = models.CharField('Código', max_length=10, blank=True)
    bandera_url = models.URLField('URL bandera', blank=True)
    api_externa_id = models.IntegerField(
        'ID en API externa',
        unique=True,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
