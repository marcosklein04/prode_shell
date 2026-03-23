"""Serializers para salas."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import MiembroSala, Sala

Usuario = get_user_model()


class SalaCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear una sala."""

    class Meta:
        model = Sala
        fields = ['nombre', 'descripcion', 'es_publica', 'max_miembros']


class SalaSerializer(serializers.ModelSerializer):
    """Serializer completo de sala."""

    creador_nombre = serializers.CharField(source='creador.nombre_completo', read_only=True)
    cantidad_miembros = serializers.IntegerField(read_only=True)
    mi_rol = serializers.SerializerMethodField()

    class Meta:
        model = Sala
        fields = [
            'id', 'nombre', 'descripcion', 'codigo', 'creador_nombre',
            'es_publica', 'max_miembros', 'cantidad_miembros',
            'activa', 'mi_rol', 'created_at',
        ]

    def get_mi_rol(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        membresia = MiembroSala.objects.filter(
            sala=obj, usuario=request.user
        ).first()
        return membresia.rol if membresia else None


class SalaListSerializer(serializers.ModelSerializer):
    """Serializer resumido para listados."""

    creador_nombre = serializers.CharField(source='creador.nombre_completo', read_only=True)
    cantidad_miembros = serializers.IntegerField(read_only=True)

    class Meta:
        model = Sala
        fields = [
            'id', 'nombre', 'descripcion', 'creador_nombre',
            'es_publica', 'cantidad_miembros', 'activa', 'created_at',
        ]


class UnirseSalaSerializer(serializers.Serializer):
    """Serializer para unirse a una sala por código."""

    codigo = serializers.CharField(max_length=20)


class MiembroSalaSerializer(serializers.ModelSerializer):
    """Serializer de miembro de sala."""

    email = serializers.CharField(source='usuario.email', read_only=True)
    nombre_completo = serializers.CharField(source='usuario.nombre_completo', read_only=True)
    puntos_totales = serializers.IntegerField(source='usuario.puntos_totales', read_only=True)

    class Meta:
        model = MiembroSala
        fields = ['id', 'email', 'nombre_completo', 'puntos_totales', 'rol', 'created_at']


class RankingSalaSerializer(serializers.ModelSerializer):
    """Serializer para ranking dentro de una sala."""

    nombre_completo = serializers.CharField(read_only=True)
    posicion = serializers.SerializerMethodField()

    class Meta:
        model = Usuario
        fields = ['id', 'nombre_completo', 'first_name', 'last_name', 'puntos_totales', 'posicion']

    def get_posicion(self, obj):
        if hasattr(obj, '_posicion'):
            return obj._posicion
        return None


class ExpulsarMiembroSerializer(serializers.Serializer):
    """Serializer para expulsar a un miembro."""

    usuario_id = serializers.IntegerField()
