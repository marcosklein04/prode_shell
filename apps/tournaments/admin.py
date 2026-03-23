"""Configuración del admin para torneos."""

from django.contrib import admin

from .models import Equipo, Fase, Torneo


class FaseInline(admin.TabularInline):
    model = Fase
    extra = 0


@admin.register(Torneo)
class TorneoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'temporada', 'activo', 'created_at']
    list_filter = ['activo', 'temporada']
    inlines = [FaseInline]


@admin.register(Fase)
class FaseAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'torneo', 'orden']
    list_filter = ['torneo']


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'api_externa_id']
    search_fields = ['nombre', 'codigo']
