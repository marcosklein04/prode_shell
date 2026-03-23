"""Tests para servicios de ranking y puntaje."""

import pytest
from django.contrib.auth import get_user_model

from apps.predictions.models import Pronostico
from apps.rankings.models import ReglaPuntaje
from apps.rankings.services import (
    calcular_puntos_pronostico,
    obtener_posicion_usuario,
    recalcular_puntos_partido,
)

Usuario = get_user_model()


@pytest.mark.django_db
class TestCalcularPuntos:

    def setup_method(self):
        self.puntos_config = {
            'resultado_exacto': 3,
            'acierto_ganador': 1,
        }

    def test_resultado_exacto(self, usuario, partido_finalizado):
        # Partido: 2-1
        pronostico = Pronostico.objects.create(
            usuario=usuario,
            partido=partido_finalizado,
            goles_local=2,
            goles_visitante=1,
        )
        puntos = calcular_puntos_pronostico(pronostico, self.puntos_config)
        assert puntos == 3

    def test_acierta_ganador(self, usuario, partido_finalizado):
        # Partido: 2-1, pronóstico: 1-0 (acierta local gana)
        pronostico = Pronostico.objects.create(
            usuario=usuario,
            partido=partido_finalizado,
            goles_local=1,
            goles_visitante=0,
        )
        puntos = calcular_puntos_pronostico(pronostico, self.puntos_config)
        assert puntos == 1

    def test_error_total(self, usuario, partido_finalizado):
        # Partido: 2-1, pronóstico: 0-3
        pronostico = Pronostico.objects.create(
            usuario=usuario,
            partido=partido_finalizado,
            goles_local=0,
            goles_visitante=3,
        )
        puntos = calcular_puntos_pronostico(pronostico, self.puntos_config)
        assert puntos == 0

    def test_partido_sin_resultado(self, usuario, partido):
        pronostico = Pronostico.objects.create(
            usuario=usuario,
            partido=partido,
            goles_local=2,
            goles_visitante=1,
        )
        puntos = calcular_puntos_pronostico(pronostico, self.puntos_config)
        assert puntos is None


@pytest.mark.django_db
class TestRecalcularPuntosPartido:

    def test_recalcula_y_actualiza_usuario(self, usuario, partido_finalizado, torneo):
        # Crear reglas
        ReglaPuntaje.objects.create(
            torneo=torneo,
            tipo=ReglaPuntaje.TipoRegla.RESULTADO_EXACTO,
            puntos=3,
        )
        ReglaPuntaje.objects.create(
            torneo=torneo,
            tipo=ReglaPuntaje.TipoRegla.ACIERTO_GANADOR,
            puntos=1,
        )

        # Crear pronóstico exacto
        Pronostico.objects.create(
            usuario=usuario,
            partido=partido_finalizado,
            goles_local=2,
            goles_visitante=1,
        )

        recalcular_puntos_partido(partido_finalizado)

        usuario.refresh_from_db()
        assert usuario.puntos_totales == 3


@pytest.mark.django_db
class TestObtenerPosicion:

    def test_posicion_unico_usuario(self, usuario):
        data = obtener_posicion_usuario(usuario)
        assert data['posicion'] == 1
        assert data['total_participantes'] == 1
