"""Configuración del admin para partidos."""

from django.contrib import admin

from .models import Partido


@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = [
        'equipo_local', 'equipo_visitante', 'fase',
        'fecha_hora', 'estado', 'goles_local', 'goles_visitante',
    ]
    list_filter = ['estado', 'fase', 'fase__torneo']
    search_fields = ['equipo_local__nombre', 'equipo_visitante__nombre']
    date_hierarchy = 'fecha_hora'
    raw_id_fields = ['equipo_local', 'equipo_visitante']
