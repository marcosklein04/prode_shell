"""Serializers para rankings."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

Usuario = get_user_model()


class RankingSerializer(serializers.ModelSerializer):
    """Serializer para cada entrada del ranking."""

    nombre_completo = serializers.CharField(read_only=True)
    posicion = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'nombre_completo', 'first_name', 'last_name', 'puntos_totales', 'posicion']

    def get_posicion(self, obj):
        # La posición se asigna en la vista basándose en el orden
        if hasattr(obj, '_posicion'):
            return obj._posicion
        return None


class MiRankingSerializer(serializers.Serializer):
    """Serializer para la posición del usuario actual."""

    posicion = serializers.IntegerField()
    puntos_totales = serializers.IntegerField()
    total_participantes = serializers.IntegerField()
