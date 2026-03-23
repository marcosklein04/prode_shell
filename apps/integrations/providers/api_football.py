"""Proveedor concreto: API-Football (api-sports.io)."""

import logging
from datetime import datetime

import requests
from django.conf import settings

from .base import BaseFootballProvider

logger = logging.getLogger(__name__)

# Mapeo de estados de API-Football a estados internos
ESTADO_MAP = {
    'TBD': 'programado',
    'NS': 'programado',
    'scheduled': 'programado',
    '1H': 'en_juego',
    '2H': 'en_juego',
    'HT': 'en_juego',
    'ET': 'en_juego',
    'P': 'en_juego',
    'BT': 'en_juego',
    'LIVE': 'en_juego',
    'FT': 'finalizado',
    'AET': 'finalizado',
    'PEN': 'finalizado',
    'SUSP': 'suspendido',
    'INT': 'suspendido',
    'PST': 'postergado',
    'CANC': 'cancelado',
    'ABD': 'cancelado',
    'AWD': 'finalizado',
    'WO': 'finalizado',
}


class ApiFootballProvider(BaseFootballProvider):
    """Implementación del proveedor usando API-Football (api-sports.io)."""

    NOMBRE_PROVEEDOR = 'api-football'

    def __init__(self):
        self.api_key = settings.FOOTBALL_API_KEY
        self.base_url = settings.FOOTBALL_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'x-apisports-key': self.api_key,
        })

    def _hacer_request(self, endpoint, params=None):
        """Realiza una petición a la API."""
        url = f'{self.base_url}/{endpoint}'
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get('errors'):
                logger.error(f'API-Football error: {data["errors"]}')
                raise Exception(f'Error de API-Football: {data["errors"]}')

            return data.get('response', [])

        except requests.RequestException as e:
            logger.error(f'Error de conexión con API-Football: {e}')
            raise

    def _mapear_estado(self, status_short):
        """Mapea estado de API-Football a estado interno."""
        return ESTADO_MAP.get(status_short, 'programado')

    def obtener_equipos(self, league_id, season):
        """Obtiene equipos desde API-Football."""
        raw_data = self._hacer_request('teams', {
            'league': league_id,
            'season': season,
        })

        equipos = []
        for item in raw_data:
            team = item.get('team', {})
            equipos.append({
                'api_externa_id': team.get('id'),
                'nombre': team.get('name', ''),
                'codigo': team.get('code', ''),
                'bandera_url': team.get('logo', ''),
            })

        return equipos

    def obtener_partidos(self, league_id, season):
        """Obtiene partidos desde API-Football."""
        raw_data = self._hacer_request('fixtures', {
            'league': league_id,
            'season': season,
        })

        partidos = []
        for item in raw_data:
            fixture = item.get('fixture', {})
            teams = item.get('teams', {})
            goals = item.get('goals', {})
            league_data = item.get('league', {})

            fecha_str = fixture.get('date', '')
            try:
                fecha_hora = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                fecha_hora = None

            status_short = fixture.get('status', {}).get('short', 'NS')

            partidos.append({
                'api_externa_id': fixture.get('id'),
                'equipo_local_api_id': teams.get('home', {}).get('id'),
                'equipo_visitante_api_id': teams.get('away', {}).get('id'),
                'fecha_hora': fecha_hora,
                'estado': self._mapear_estado(status_short),
                'goles_local': goals.get('home'),
                'goles_visitante': goals.get('away'),
                'fase_nombre': league_data.get('round', 'Fase de grupos'),
            })

        return partidos

    def obtener_resultados(self, league_id, season):
        """Obtiene solo resultados actualizados desde API-Football."""
        raw_data = self._hacer_request('fixtures', {
            'league': league_id,
            'season': season,
        })

        resultados = []
        for item in raw_data:
            fixture = item.get('fixture', {})
            goals = item.get('goals', {})
            status_short = fixture.get('status', {}).get('short', 'NS')

            resultados.append({
                'api_externa_id': fixture.get('id'),
                'estado': self._mapear_estado(status_short),
                'goles_local': goals.get('home'),
                'goles_visitante': goals.get('away'),
            })

        return resultados
