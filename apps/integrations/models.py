"""Modelos de log de sincronización."""

from django.db import models

from core.mixins import TimestampMixin


class LogSincronizacion(TimestampMixin):
    """Registro de cada operación de sincronización con la API externa."""

    class Estado(models.TextChoices):
        EN_PROGRESO = 'en_progreso', 'En progreso'
        EXITOSO = 'exitoso', 'Exitoso'
        FALLO_PARCIAL = 'fallo_parcial', 'Fallo parcial'
        FALLIDO = 'fallido', 'Fallido'

    class TipoEntidad(models.TextChoices):
        EQUIPOS = 'equipos', 'Equipos'
        PARTIDOS = 'partidos', 'Partidos'
        RESULTADOS = 'resultados', 'Resultados'

    proveedor = models.CharField('Proveedor', max_length=100)
    tipo_entidad = models.CharField(
        'Tipo de entidad',
        max_length=30,
        choices=TipoEntidad.choices,
    )
    estado = models.CharField(
        'Estado',
        max_length=20,
        choices=Estado.choices,
        default=Estado.EN_PROGRESO,
    )
    registros_procesados = models.IntegerField('Registros procesados', default=0)
    detalle_error = models.TextField('Detalle de error', blank=True)
    inicio = models.DateTimeField('Inicio', auto_now_add=True)
    fin = models.DateTimeField('Fin', null=True, blank=True)

    class Meta:
        verbose_name = 'Log de sincronización'
        verbose_name_plural = 'Logs de sincronización'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.proveedor} - {self.tipo_entidad} - {self.get_estado_display()}'
