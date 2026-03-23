"""Permisos personalizados para la API."""

from rest_framework.permissions import BasePermission


class EsAdmin(BasePermission):
    """Permite acceso solo a usuarios con rol admin."""

    message = 'Solo los administradores pueden realizar esta acción.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.es_admin
        )


class EsPropietario(BasePermission):
    """Permite acceso solo al propietario del recurso."""

    message = 'Solo podés acceder a tus propios recursos.'

    def has_object_permission(self, request, view, obj):
        return obj.usuario == request.user
