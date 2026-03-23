"""Vistas para pronósticos."""

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.matches.models import Partido
from core.pagination import PaginacionEstandar
from core.permissions import EsAdmin

from . import services
from .models import Pronostico
from .serializers import (
    PronosticoAdminSerializer,
    PronosticoCreateSerializer,
    PronosticoSerializer,
    PronosticoUpdateSerializer,
)


@extend_schema(tags=['Pronósticos'])
class PronosticoCreateView(generics.CreateAPIView):
    """Crear un nuevo pronóstico."""

    serializer_class = PronosticoCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        partido = get_object_or_404(Partido, id=serializer.validated_data['partido_id'])

        pronostico = services.crear_pronostico(
            usuario=request.user,
            partido=partido,
            goles_local=serializer.validated_data['goles_local'],
            goles_visitante=serializer.validated_data['goles_visitante'],
        )

        return Response(
            PronosticoSerializer(pronostico).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=['Pronósticos'])
class PronosticoUpdateView(generics.UpdateAPIView):
    """Actualizar un pronóstico existente."""

    serializer_class = PronosticoUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pronostico.objects.filter(usuario=self.request.user)

    def update(self, request, *args, **kwargs):
        pronostico = self.get_object()
        serializer = self.get_serializer(pronostico, data=request.data)
        serializer.is_valid(raise_exception=True)

        pronostico = services.actualizar_pronostico(
            pronostico=pronostico,
            goles_local=serializer.validated_data['goles_local'],
            goles_visitante=serializer.validated_data['goles_visitante'],
        )

        return Response(PronosticoSerializer(pronostico).data)


@extend_schema_view(
    get=extend_schema(tags=['Pronósticos']),
)
class MisPronosticosView(generics.ListAPIView):
    """Listar todos los pronósticos del usuario autenticado."""

    serializer_class = PronosticoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginacionEstandar

    def get_queryset(self):
        return Pronostico.objects.filter(
            usuario=self.request.user
        ).select_related(
            'partido', 'partido__equipo_local',
            'partido__equipo_visitante', 'partido__fase',
        )


@extend_schema(tags=['Pronósticos'])
class MiPronosticoPartidoView(generics.RetrieveAPIView):
    """Obtener el pronóstico del usuario para un partido específico."""

    serializer_class = PronosticoSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(
            Pronostico.objects.select_related(
                'partido', 'partido__equipo_local',
                'partido__equipo_visitante', 'partido__fase',
            ),
            usuario=self.request.user,
            partido_id=self.kwargs['match_id'],
        )


@extend_schema_view(
    get=extend_schema(tags=['Admin']),
)
class AdminPronosticosView(generics.ListAPIView):
    """Listar todos los pronósticos (solo admin)."""

    serializer_class = PronosticoAdminSerializer
    permission_classes = [IsAuthenticated, EsAdmin]
    pagination_class = PaginacionEstandar
    filterset_fields = ['partido', 'usuario']

    def get_queryset(self):
        return Pronostico.objects.select_related(
            'usuario', 'partido', 'partido__equipo_local',
            'partido__equipo_visitante', 'partido__fase',
        ).all()
