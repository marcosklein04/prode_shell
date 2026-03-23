"""Serializers para torneos, fases y equipos."""

from rest_framework import serializers

from .models import Equipo, Fase, Torneo


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'codigo', 'bandera_url']


class FaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fase
        fields = ['id', 'nombre', 'orden']


class TorneoSerializer(serializers.ModelSerializer):
    fases = FaseSerializer(many=True, read_only=True)

    class Meta:
        model = Torneo
        fields = ['id', 'nombre', 'temporada', 'activo', 'fases']
