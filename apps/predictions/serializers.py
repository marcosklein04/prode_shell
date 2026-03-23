"""Serializers para pronósticos."""

from rest_framework import serializers

from apps.matches.serializers import PartidoListSerializer

from .models import Pronostico


class PronosticoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear un pronóstico."""

    partido_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Pronostico
        fields = ['partido_id', 'goles_local', 'goles_visitante']

    def validate_goles_local(self, value):
        if value < 0:
            raise serializers.ValidationError('Los goles no pueden ser negativos.')
        return value

    def validate_goles_visitante(self, value):
        if value < 0:
            raise serializers.ValidationError('Los goles no pueden ser negativos.')
        return value


class PronosticoUpdateSerializer(serializers.ModelSerializer):
    """Serializer para actualizar un pronóstico."""

    class Meta:
        model = Pronostico
        fields = ['goles_local', 'goles_visitante']


class PronosticoSerializer(serializers.ModelSerializer):
    """Serializer completo de pronóstico con datos del partido."""

    partido = PartidoListSerializer(read_only=True)

    class Meta:
        model = Pronostico
        fields = [
            'id', 'partido', 'goles_local', 'goles_visitante',
            'puntos', 'created_at', 'updated_at',
        ]


class PronosticoAdminSerializer(serializers.ModelSerializer):
    """Serializer de pronóstico para admin."""

    partido = PartidoListSerializer(read_only=True)
    usuario_email = serializers.CharField(source='usuario.email', read_only=True)
    usuario_nombre = serializers.CharField(source='usuario.nombre_completo', read_only=True)

    class Meta:
        model = Pronostico
        fields = [
            'id', 'usuario_email', 'usuario_nombre',
            'partido', 'goles_local', 'goles_visitante',
            'puntos', 'created_at',
        ]
