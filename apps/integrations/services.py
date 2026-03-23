"""Servicios de sincronización con la API externa."""

import logging

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from apps.matches.models import Partido
from apps.rankings import services as ranking_services
from apps.tournaments.models import Equipo, Fase, Torneo

from .models import LogSincronizacion
from .providers import ApiFootballProvider

logger = logging.getLogger(__name__)


def obtener_proveedor():
    """Factory para obtener el proveedor de datos configurado."""
    return ApiFootballProvider()


def obtener_o_crear_torneo():
    """Obtiene o crea el torneo configurado."""
    torneo, _ = Torneo.objects.get_or_create(
        api_externa_id=settings.FOOTBALL_API_LEAGUE_ID,
        defaults={
            'nombre': 'Copa Mundial FIFA 2026',
            'temporada': settings.FOOTBALL_API_SEASON,
            'activo': True,
        },
    )
    return torneo


@transaction.atomic
def sincronizar_equipos():
    """Sincroniza equipos desde la API externa."""
    log = LogSincronizacion.objects.create(
        proveedor=ApiFootballProvider.NOMBRE_PROVEEDOR,
        tipo_entidad=LogSincronizacion.TipoEntidad.EQUIPOS,
        estado=LogSincronizacion.Estado.EN_PROGRESO,
    )

    try:
        proveedor = obtener_proveedor()
        equipos_data = proveedor.obtener_equipos(
            settings.FOOTBALL_API_LEAGUE_ID,
            settings.FOOTBALL_API_SEASON,
        )

        procesados = 0
        for data in equipos_data:
            Equipo.objects.update_or_create(
                api_externa_id=data['api_externa_id'],
                defaults={
                    'nombre': data['nombre'],
                    'codigo': data['codigo'],
                    'bandera_url': data['bandera_url'],
                },
            )
            procesados += 1

        log.estado = LogSincronizacion.Estado.EXITOSO
        log.registros_procesados = procesados
        log.fin = timezone.now()
        log.save()

        logger.info(f'Equipos sincronizados: {procesados}')
        return procesados

    except Exception as e:
        log.estado = LogSincronizacion.Estado.FALLIDO
        log.detalle_error = str(e)
        log.fin = timezone.now()
        log.save()
        logger.error(f'Error sincronizando equipos: {e}')
        raise


@transaction.atomic
def sincronizar_partidos():
    """Sincroniza partidos desde la API externa."""
    log = LogSincronizacion.objects.create(
        proveedor=ApiFootballProvider.NOMBRE_PROVEEDOR,
        tipo_entidad=LogSincronizacion.TipoEntidad.PARTIDOS,
        estado=LogSincronizacion.Estado.EN_PROGRESO,
    )

    try:
        proveedor = obtener_proveedor()
        torneo = obtener_o_crear_torneo()

        partidos_data = proveedor.obtener_partidos(
            settings.FOOTBALL_API_LEAGUE_ID,
            settings.FOOTBALL_API_SEASON,
        )

        procesados = 0
        errores = []

        for data in partidos_data:
            try:
                equipo_local = Equipo.objects.get(api_externa_id=data['equipo_local_api_id'])
                equipo_visitante = Equipo.objects.get(api_externa_id=data['equipo_visitante_api_id'])
            except Equipo.DoesNotExist:
                errores.append(
                    f'Equipo no encontrado para partido {data["api_externa_id"]}'
                )
                continue

            # Obtener o crear fase
            fase, _ = Fase.objects.get_or_create(
                torneo=torneo,
                nombre=data['fase_nombre'],
                defaults={'orden': 0},
            )

            Partido.objects.update_or_create(
                api_externa_id=data['api_externa_id'],
                defaults={
                    'fase': fase,
                    'equipo_local': equipo_local,
                    'equipo_visitante': equipo_visitante,
                    'fecha_hora': data['fecha_hora'],
                    'estado': data['estado'],
                    'goles_local': data['goles_local'],
                    'goles_visitante': data['goles_visitante'],
                },
            )
            procesados += 1

        if errores:
            log.estado = LogSincronizacion.Estado.FALLO_PARCIAL
            log.detalle_error = '\n'.join(errores)
        else:
            log.estado = LogSincronizacion.Estado.EXITOSO

        log.registros_procesados = procesados
        log.fin = timezone.now()
        log.save()

        logger.info(f'Partidos sincronizados: {procesados}, errores: {len(errores)}')
        return procesados

    except Exception as e:
        log.estado = LogSincronizacion.Estado.FALLIDO
        log.detalle_error = str(e)
        log.fin = timezone.now()
        log.save()
        logger.error(f'Error sincronizando partidos: {e}')
        raise


@transaction.atomic
def sincronizar_resultados():
    """
    Sincroniza resultados de partidos y recalcula puntos
    de los partidos que pasaron a finalizado.
    """
    log = LogSincronizacion.objects.create(
        proveedor=ApiFootballProvider.NOMBRE_PROVEEDOR,
        tipo_entidad=LogSincronizacion.TipoEntidad.RESULTADOS,
        estado=LogSincronizacion.Estado.EN_PROGRESO,
    )

    try:
        proveedor = obtener_proveedor()
        resultados_data = proveedor.obtener_resultados(
            settings.FOOTBALL_API_LEAGUE_ID,
            settings.FOOTBALL_API_SEASON,
        )

        procesados = 0
        partidos_finalizados = []

        for data in resultados_data:
            try:
                partido = Partido.objects.get(api_externa_id=data['api_externa_id'])
            except Partido.DoesNotExist:
                continue

            estado_anterior = partido.estado
            partido.estado = data['estado']
            partido.goles_local = data['goles_local']
            partido.goles_visitante = data['goles_visitante']
            partido.save(update_fields=[
                'estado', 'goles_local', 'goles_visitante', 'updated_at'
            ])
            procesados += 1

            # Si el partido pasó a finalizado, recalcular puntos
            if (estado_anterior != Partido.Estado.FINALIZADO
                    and partido.estado == Partido.Estado.FINALIZADO):
                partidos_finalizados.append(partido)

        # Recalcular puntos de partidos recién finalizados
        for partido in partidos_finalizados:
            ranking_services.recalcular_puntos_partido(partido)

        log.estado = LogSincronizacion.Estado.EXITOSO
        log.registros_procesados = procesados
        log.fin = timezone.now()
        log.save()

        logger.info(
            f'Resultados sincronizados: {procesados}, '
            f'partidos finalizados: {len(partidos_finalizados)}'
        )
        return {
            'procesados': procesados,
            'partidos_finalizados': len(partidos_finalizados),
        }

    except Exception as e:
        log.estado = LogSincronizacion.Estado.FALLIDO
        log.detalle_error = str(e)
        log.fin = timezone.now()
        log.save()
        logger.error(f'Error sincronizando resultados: {e}')
        raise
