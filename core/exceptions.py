"""Excepciones personalizadas del dominio."""

from rest_framework.exceptions import APIException


class PronosticoCerradoError(APIException):
    """Se lanza cuando se intenta pronosticar un partido ya iniciado o finalizado."""

    status_code = 400
    default_detail = 'No se puede pronosticar un partido que ya comenzó o finalizó.'
    default_code = 'pronostico_cerrado'


class PronosticoDuplicadoError(APIException):
    """Se lanza cuando un usuario ya tiene pronóstico para ese partido."""

    status_code = 400
    default_detail = 'Ya tenés un pronóstico para este partido.'
    default_code = 'pronostico_duplicado'


class SincronizacionError(APIException):
    """Se lanza cuando falla la sincronización con la API externa."""

    status_code = 502
    default_detail = 'Error al sincronizar datos con el proveedor externo.'
    default_code = 'sincronizacion_error'
