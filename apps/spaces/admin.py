"""Configuración del admin para salas."""

from django.contrib import admin

from .models import MiembroSala, Sala


class MiembroInline(admin.TabularInline):
    model = MiembroSala
    extra = 0
    raw_id_fields = ['usuario']


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'creador', 'codigo', 'es_publica', 'cantidad_miembros', 'activa', 'created_at']
    list_filter = ['es_publica', 'activa']
    search_fields = ['nombre', 'codigo', 'creador__email']
    readonly_fields = ['codigo']
    raw_id_fields = ['creador']
    inlines = [MiembroInline]


@admin.register(MiembroSala)
class MiembroSalaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'sala', 'rol', 'created_at']
    list_filter = ['rol', 'sala']
    raw_id_fields = ['usuario', 'sala']
