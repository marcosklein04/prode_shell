"""Servicios de negocio para pronósticos."""

from core.exceptions import PronosticoCerradoError, PronosticoDuplicadoError

from .models import Pronostico


def crear_pronostico(usuario, partido, goles_local, goles_visitante):
    """
    Crea un pronóstico para un usuario y partido.

    Validaciones:
    - El partido debe estar abierto para pronósticos
    - El usuario no debe tener ya un pronóstico para ese partido
    """
    if not partido.esta_abierto_para_pronosticos:
        raise PronosticoCerradoError()

    if Pronostico.objects.filter(usuario=usuario, partido=partido).exists():
        raise PronosticoDuplicadoError()

    return Pronostico.objects.create(
        usuario=usuario,
        partido=partido,
        goles_local=goles_local,
        goles_visitante=goles_visitante,
    )


def actualizar_pronostico(pronostico, goles_local, goles_visitante):
    """
    Actualiza un pronóstico existente.

    Solo se puede actualizar si el partido sigue abierto.
    """
    if not pronostico.partido.esta_abierto_para_pronosticos:
        raise PronosticoCerradoError(
            detail='No se puede modificar un pronóstico de un partido que ya comenzó o finalizó.'
        )

    pronostico.goles_local = goles_local
    pronostico.goles_visitante = goles_visitante
    pronostico.save(update_fields=['goles_local', 'goles_visitante', 'updated_at'])
    return pronostico
