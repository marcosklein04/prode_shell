"""Configuración del admin para logs de sincronización."""

from django.contrib import admin

from .models import LogSincronizacion


@admin.register(LogSincronizacion)
class LogSincronizacionAdmin(admin.ModelAdmin):
    list_display = [
        'proveedor', 'tipo_entidad', 'estado',
        'registros_procesados', 'inicio', 'fin',
    ]
    list_filter = ['proveedor', 'tipo_entidad', 'estado']
    readonly_fields = [
        'proveedor', 'tipo_entidad', 'estado',
        'registros_procesados', 'detalle_error',
        'inicio', 'fin',
    ]
