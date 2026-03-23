"""Configuración del admin para reglas de puntaje."""

from django.contrib import admin

from .models import ReglaPuntaje


@admin.register(ReglaPuntaje)
class ReglaPuntajeAdmin(admin.ModelAdmin):
    list_display = ['torneo', 'tipo', 'puntos', 'descripcion']
    list_filter = ['torneo', 'tipo']
