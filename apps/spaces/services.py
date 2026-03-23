"""Servicios de negocio para salas."""

from django.db.models import Sum
from rest_framework.exceptions import ValidationError

from apps.predictions.models import Pronostico

from .models import MiembroSala, Sala


def crear_sala(usuario, nombre, descripcion='', es_publica=False, max_miembros=100):
    """Crea una sala y agrega al creador como admin."""
    sala = Sala.objects.create(
        nombre=nombre,
        descripcion=descripcion,
        creador=usuario,
        es_publica=es_publica,
        max_miembros=max_miembros,
    )
    MiembroSala.objects.create(
        sala=sala,
        usuario=usuario,
        rol=MiembroSala.Rol.ADMIN,
    )
    return sala


def unirse_a_sala(usuario, codigo):
    """Un usuario se une a una sala usando el código de invitación."""
    try:
        sala = Sala.objects.get(codigo=codigo, activa=True)
    except Sala.DoesNotExist:
        raise ValidationError({'codigo': 'Código de sala inválido o sala inactiva.'})

    if MiembroSala.objects.filter(sala=sala, usuario=usuario).exists():
        raise ValidationError({'detail': 'Ya sos miembro de esta sala.'})

    if sala.cantidad_miembros >= sala.max_miembros:
        raise ValidationError({'detail': 'La sala está llena.'})

    MiembroSala.objects.create(
        sala=sala,
        usuario=usuario,
        rol=MiembroSala.Rol.MIEMBRO,
    )
    return sala


def salir_de_sala(usuario, sala):
    """Un usuario abandona una sala."""
    membresia = MiembroSala.objects.filter(sala=sala, usuario=usuario).first()
    if not membresia:
        raise ValidationError({'detail': 'No sos miembro de esta sala.'})

    if membresia.rol == MiembroSala.Rol.ADMIN and sala.miembros.count() > 1:
        # Si es el admin y hay otros miembros, transferir admin al más antiguo
        siguiente = MiembroSala.objects.filter(
            sala=sala
        ).exclude(usuario=usuario).order_by('created_at').first()
        if siguiente:
            siguiente.rol = MiembroSala.Rol.ADMIN
            siguiente.save(update_fields=['rol', 'updated_at'])

    membresia.delete()


def obtener_ranking_sala(sala):
    """
    Ranking de una sala: ordena los miembros por sus puntos totales
    (usa el campo puntos_totales del usuario).
    """
    miembros_ids = sala.miembros.values_list('usuario_id', flat=True)
    from django.contrib.auth import get_user_model
    Usuario = get_user_model()

    return Usuario.objects.filter(
        id__in=miembros_ids,
        is_active=True,
    ).order_by('-puntos_totales', 'last_name', 'first_name')


def expulsar_miembro(sala, admin_usuario, usuario_a_expulsar):
    """Un admin de sala expulsa a un miembro."""
    admin_membresia = MiembroSala.objects.filter(
        sala=sala, usuario=admin_usuario, rol=MiembroSala.Rol.ADMIN
    ).first()
    if not admin_membresia:
        raise ValidationError({'detail': 'No tenés permisos de administrador en esta sala.'})

    if admin_usuario == usuario_a_expulsar:
        raise ValidationError({'detail': 'No podés expulsarte a vos mismo.'})

    membresia = MiembroSala.objects.filter(sala=sala, usuario=usuario_a_expulsar).first()
    if not membresia:
        raise ValidationError({'detail': 'El usuario no es miembro de esta sala.'})

    membresia.delete()
