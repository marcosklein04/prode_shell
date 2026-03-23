"""Serializers para integraciones."""

from rest_framework import serializers

from .models import LogSincronizacion


class LogSincronizacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSincronizacion
        fields = [
            'id', 'proveedor', 'tipo_entidad', 'estado',
            'registros_procesados', 'detalle_error',
            'inicio', 'fin', 'created_at',
        ]
