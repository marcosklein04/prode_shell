"""Serializers para autenticación y usuarios."""

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

Usuario = get_user_model()


class RegistroSerializer(serializers.ModelSerializer):
    """Serializer para registro de nuevos usuarios."""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        validators=[validate_password],
        style={'input_type': 'password'},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'Las contraseñas no coinciden.',
            })
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        return Usuario.objects.create_user(**validated_data)


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer público de usuario (sin datos sensibles)."""

    nombre_completo = serializers.CharField(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'nombre_completo', 'rol', 'puntos_totales',
            'date_joined',
        ]
        read_only_fields = ['id', 'email', 'rol', 'puntos_totales', 'date_joined']


class UsuarioAdminSerializer(serializers.ModelSerializer):
    """Serializer para vista admin con todos los campos."""

    nombre_completo = serializers.CharField(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'nombre_completo', 'rol', 'puntos_totales',
            'is_active', 'date_joined', 'last_login',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
