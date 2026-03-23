"""Clase base abstracta para proveedores de datos de fútbol."""

from abc import ABC, abstractmethod


class BaseFootballProvider(ABC):
    """
    Interfaz abstracta para proveedores de datos de fútbol.
    Cada proveedor concreto implementa estos métodos mapeando
    los datos externos al formato interno de la aplicación.
    """

    @abstractmethod
    def obtener_equipos(self, league_id, season):
        """
        Obtiene los equipos de un torneo.

        Retorna lista de dicts con formato:
        [
            {
                'api_externa_id': int,
                'nombre': str,
                'codigo': str,
                'bandera_url': str,
            },
            ...
        ]
        """
        pass

    @abstractmethod
    def obtener_partidos(self, league_id, season):
        """
        Obtiene todos los partidos de un torneo.

        Retorna lista de dicts con formato:
        [
            {
                'api_externa_id': int,
                'equipo_local_api_id': int,
                'equipo_visitante_api_id': int,
                'fecha_hora': datetime,
                'estado': str,  # mapeado a Estado del modelo
                'goles_local': int | None,
                'goles_visitante': int | None,
                'fase_nombre': str,
            },
            ...
        ]
        """
        pass

    @abstractmethod
    def obtener_resultados(self, league_id, season):
        """
        Obtiene resultados actualizados de partidos finalizados.

        Retorna lista de dicts con formato:
        [
            {
                'api_externa_id': int,
                'estado': str,
                'goles_local': int | None,
                'goles_visitante': int | None,
            },
            ...
        ]
        """
        pass
