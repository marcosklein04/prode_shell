"""Configuración del admin para pronósticos."""

from django.contrib import admin

from .models import Pronostico


@admin.register(Pronostico)
class PronosticoAdmin(admin.ModelAdmin):
    list_display = [
        'usuario', 'partido', 'goles_local',
        'goles_visitante', 'puntos', 'created_at',
    ]
    list_filter = ['puntos', 'partido__fase']
    search_fields = ['usuario__email', 'usuario__first_name']
    raw_id_fields = ['usuario', 'partido']
