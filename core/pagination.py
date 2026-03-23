"""Paginación personalizada para la API."""

from rest_framework.pagination import PageNumberPagination


class PaginacionEstandar(PageNumberPagination):
    """Paginación estándar con tamaño configurable por query param."""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class PaginacionPequena(PageNumberPagination):
    """Paginación para listados cortos (top 10, top 20)."""

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
