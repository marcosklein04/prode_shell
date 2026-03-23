"""Filtros para partidos."""

import django_filters
from django.db import models

from .models import Partido


class PartidoFilter(django_filters.FilterSet):
    """Filtros para buscar partidos."""

    fase = django_filters.NumberFilter(field_name='fase__id')
    fase_nombre = django_filters.CharFilter(field_name='fase__nombre', lookup_expr='icontains')
    estado = django_filters.ChoiceFilter(choices=Partido.Estado.choices)
    equipo = django_filters.NumberFilter(method='filtrar_por_equipo')
    fecha_desde = django_filters.DateTimeFilter(field_name='fecha_hora', lookup_expr='gte')
    fecha_hasta = django_filters.DateTimeFilter(field_name='fecha_hora', lookup_expr='lte')

    class Meta:
        model = Partido
        fields = ['fase', 'fase_nombre', 'estado', 'equipo', 'fecha_desde', 'fecha_hasta']

    def filtrar_por_equipo(self, queryset, name, value):
        """Filtra partidos donde el equipo juega como local o visitante."""
        return queryset.filter(
            models.Q(equipo_local_id=value) | models.Q(equipo_visitante_id=value)
        )
