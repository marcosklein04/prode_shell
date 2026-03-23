"""Tests para servicios de pronósticos."""

import pytest
from django.utils import timezone

from apps.matches.models import Partido
from apps.predictions.models import Pronostico
from apps.predictions.services import actualizar_pronostico, crear_pronostico
from core.exceptions import PronosticoCerradoError, PronosticoDuplicadoError


@pytest.mark.django_db
class TestCrearPronostico:

    def test_crear_pronostico_exitoso(self, usuario, partido):
        pronostico = crear_pronostico(usuario, partido, 2, 1)
        assert pronostico.goles_local == 2
        assert pronostico.goles_visitante == 1
        assert pronostico.usuario == usuario
        assert pronostico.partido == partido

    def test_no_permite_pronostico_partido_finalizado(self, usuario, partido_finalizado):
        with pytest.raises(PronosticoCerradoError):
            crear_pronostico(usuario, partido_finalizado, 1, 0)

    def test_no_permite_pronostico_duplicado(self, usuario, partido):
        crear_pronostico(usuario, partido, 2, 1)
        with pytest.raises(PronosticoDuplicadoError):
            crear_pronostico(usuario, partido, 3, 0)


@pytest.mark.django_db
class TestActualizarPronostico:

    def test_actualizar_pronostico_exitoso(self, usuario, partido):
        pronostico = crear_pronostico(usuario, partido, 2, 1)
        actualizado = actualizar_pronostico(pronostico, 3, 0)
        assert actualizado.goles_local == 3
        assert actualizado.goles_visitante == 0

    def test_no_permite_actualizar_partido_finalizado(self, usuario, partido):
        pronostico = crear_pronostico(usuario, partido, 2, 1)
        partido.estado = Partido.Estado.FINALIZADO
        partido.save()

        with pytest.raises(PronosticoCerradoError):
            actualizar_pronostico(pronostico, 3, 0)
