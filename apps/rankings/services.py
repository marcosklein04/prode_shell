"""Servicios de cálculo de puntaje y ranking."""

import logging

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Sum

from apps.matches.models import Partido
from apps.predictions.models import Pronostico

from .models import ReglaPuntaje

logger = logging.getLogger(__name__)
Usuario = get_user_model()

# Puntos por defecto si no hay reglas configuradas
PUNTOS_RESULTADO_EXACTO_DEFAULT = 3
PUNTOS_ACIERTO_GANADOR_DEFAULT = 1


def obtener_puntos_reglas(torneo):
    """Obtiene los puntos configurados para cada tipo de regla."""
    reglas = ReglaPuntaje.objects.filter(torneo=torneo)
    puntos = {
        'resultado_exacto': PUNTOS_RESULTADO_EXACTO_DEFAULT,
        'acierto_ganador': PUNTOS_ACIERTO_GANADOR_DEFAULT,
    }
    for regla in reglas:
        puntos[regla.tipo] = regla.puntos
    return puntos


def calcular_puntos_pronostico(pronostico, puntos_config):
    """
    Calcula los puntos de un pronóstico individual.

    Lógica:
    - Resultado exacto: máximo puntaje
    - Acierta ganador/empate sin resultado exacto: puntaje parcial
    - Error total: 0 puntos
    """
    partido = pronostico.partido

    if partido.goles_local is None or partido.goles_visitante is None:
        return None

    # Resultado exacto
    if (pronostico.goles_local == partido.goles_local
            and pronostico.goles_visitante == partido.goles_visitante):
        return puntos_config['resultado_exacto']

    # Determinar resultado real
    if partido.goles_local > partido.goles_visitante:
        resultado_real = 'local'
    elif partido.goles_local < partido.goles_visitante:
        resultado_real = 'visitante'
    else:
        resultado_real = 'empate'

    # Determinar resultado pronosticado
    if pronostico.goles_local > pronostico.goles_visitante:
        resultado_pronosticado = 'local'
    elif pronostico.goles_local < pronostico.goles_visitante:
        resultado_pronosticado = 'visitante'
    else:
        resultado_pronosticado = 'empate'

    # Acertó ganador/empate
    if resultado_real == resultado_pronosticado:
        return puntos_config['acierto_ganador']

    # Error total
    return 0


@transaction.atomic
def recalcular_puntos_partido(partido):
    """
    Recalcula los puntos de todos los pronósticos de un partido finalizado.
    Actualiza los puntos totales de cada usuario afectado.
    """
    if partido.estado != Partido.Estado.FINALIZADO:
        logger.warning(f'Partido {partido.id} no está finalizado, no se recalculan puntos.')
        return 0

    torneo = partido.fase.torneo
    puntos_config = obtener_puntos_reglas(torneo)

    pronosticos = Pronostico.objects.filter(partido=partido).select_related('usuario')
    actualizados = 0

    for pronostico in pronosticos:
        puntos = calcular_puntos_pronostico(pronostico, puntos_config)
        if puntos is not None:
            pronostico.puntos = puntos
            pronostico.save(update_fields=['puntos', 'updated_at'])
            actualizados += 1

    # Recalcular puntos totales de los usuarios afectados
    usuarios_ids = pronosticos.values_list('usuario_id', flat=True).distinct()
    recalcular_puntos_totales_usuarios(usuarios_ids)

    logger.info(f'Partido {partido.id}: {actualizados} pronósticos recalculados.')
    return actualizados


@transaction.atomic
def recalcular_todos_los_puntos():
    """
    Recalcula los puntos de todos los pronósticos de partidos finalizados
    y actualiza los puntos totales de todos los usuarios.
    """
    partidos_finalizados = Partido.objects.filter(
        estado=Partido.Estado.FINALIZADO
    ).select_related('fase__torneo')

    total_actualizados = 0
    for partido in partidos_finalizados:
        puntos_config = obtener_puntos_reglas(partido.fase.torneo)
        pronosticos = Pronostico.objects.filter(partido=partido)

        for pronostico in pronosticos:
            puntos = calcular_puntos_pronostico(pronostico, puntos_config)
            if puntos is not None:
                pronostico.puntos = puntos
                pronostico.save(update_fields=['puntos', 'updated_at'])
                total_actualizados += 1

    # Recalcular todos los usuarios
    recalcular_puntos_totales_usuarios(
        Usuario.objects.values_list('id', flat=True)
    )

    logger.info(f'Recálculo total: {total_actualizados} pronósticos actualizados.')
    return total_actualizados


def recalcular_puntos_totales_usuarios(usuarios_ids):
    """Recalcula los puntos totales de un conjunto de usuarios."""
    for usuario_id in usuarios_ids:
        total = Pronostico.objects.filter(
            usuario_id=usuario_id,
            puntos__isnull=False,
        ).aggregate(total=Sum('puntos'))['total'] or 0

        Usuario.objects.filter(id=usuario_id).update(puntos_totales=total)


def obtener_ranking(limit=None):
    """Obtiene el ranking global ordenado por puntos."""
    qs = Usuario.objects.filter(
        is_active=True, rol='user'
    ).order_by('-puntos_totales', 'last_name', 'first_name')

    if limit:
        qs = qs[:limit]

    return qs


def obtener_posicion_usuario(usuario):
    """Obtiene la posición de un usuario en el ranking."""
    posicion = Usuario.objects.filter(
        is_active=True,
        puntos_totales__gt=usuario.puntos_totales,
    ).count() + 1

    total_participantes = Usuario.objects.filter(
        is_active=True, rol='user'
    ).count()

    return {
        'posicion': posicion,
        'puntos_totales': usuario.puntos_totales,
        'total_participantes': total_participantes,
    }
