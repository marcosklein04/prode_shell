"""Serializers para partidos."""

from rest_framework import serializers

from apps.tournaments.serializers import EquipoSerializer, FaseSerializer

from .models import Partido


class PartidoSerializer(serializers.ModelSerializer):
    """Serializer completo de partido."""

    equipo_local = EquipoSerializer(read_only=True)
    equipo_visitante = EquipoSerializer(read_only=True)
    fase = FaseSerializer(read_only=True)
    esta_abierto_para_pronosticos = serializers.BooleanField(read_only=True)
    resultado_texto = serializers.CharField(read_only=True)

    class Meta:
        model = Partido
        fields = [
            'id', 'fase', 'equipo_local', 'equipo_visitante',
            'fecha_hora', 'estado', 'goles_local', 'goles_visitante',
            'esta_abierto_para_pronosticos', 'resultado_texto',
        ]


class PartidoListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listados de partidos."""

    equipo_local = EquipoSerializer(read_only=True)
    equipo_visitante = EquipoSerializer(read_only=True)
    fase_nombre = serializers.CharField(source='fase.nombre', read_only=True)
    esta_abierto_para_pronosticos = serializers.BooleanField(read_only=True)

    class Meta:
        model = Partido
        fields = [
            'id', 'fase_nombre', 'equipo_local', 'equipo_visitante',
            'fecha_hora', 'estado', 'goles_local', 'goles_visitante',
            'esta_abierto_para_pronosticos',
        ]
