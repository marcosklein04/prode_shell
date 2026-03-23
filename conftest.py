"""Fixtures compartidos para tests."""

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient

from apps.matches.models import Partido
from apps.tournaments.models import Equipo, Fase, Torneo

Usuario = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def usuario(db):
    return Usuario.objects.create_user(
        email='usuario@test.com',
        password='TestPass123!',
        first_name='Juan',
        last_name='Pérez',
    )


@pytest.fixture
def admin_usuario(db):
    return Usuario.objects.create_user(
        email='admin@test.com',
        password='AdminPass123!',
        first_name='Admin',
        last_name='Shell',
        rol=Usuario.Rol.ADMIN,
    )


@pytest.fixture
def api_client_autenticado(api_client, usuario):
    api_client.force_authenticate(user=usuario)
    return api_client


@pytest.fixture
def api_client_admin(api_client, admin_usuario):
    api_client.force_authenticate(user=admin_usuario)
    return api_client


@pytest.fixture
def torneo(db):
    return Torneo.objects.create(
        nombre='Copa Mundial FIFA 2026',
        temporada=2026,
        activo=True,
    )


@pytest.fixture
def fase(torneo):
    return Fase.objects.create(
        torneo=torneo,
        nombre='Fase de grupos',
        orden=1,
    )


@pytest.fixture
def equipo_local(db):
    return Equipo.objects.create(
        nombre='Argentina',
        codigo='ARG',
        api_externa_id=1,
    )


@pytest.fixture
def equipo_visitante(db):
    return Equipo.objects.create(
        nombre='Brasil',
        codigo='BRA',
        api_externa_id=2,
    )


@pytest.fixture
def partido(fase, equipo_local, equipo_visitante):
    return Partido.objects.create(
        fase=fase,
        equipo_local=equipo_local,
        equipo_visitante=equipo_visitante,
        fecha_hora=timezone.now() + timezone.timedelta(days=7),
        estado=Partido.Estado.PROGRAMADO,
    )


@pytest.fixture
def partido_finalizado(fase, equipo_local, equipo_visitante):
    return Partido.objects.create(
        fase=fase,
        equipo_local=equipo_local,
        equipo_visitante=equipo_visitante,
        fecha_hora=timezone.now() - timezone.timedelta(days=1),
        estado=Partido.Estado.FINALIZADO,
        goles_local=2,
        goles_visitante=1,
    )
