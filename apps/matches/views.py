"""Vistas para partidos."""

from django.utils import timezone
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.pagination import PaginacionEstandar

from .filters import PartidoFilter
from .models import Partido
from .serializers import PartidoListSerializer, PartidoSerializer


@extend_schema_view(
    get=extend_schema(tags=['Partidos']),
)
class PartidoListView(generics.ListAPIView):
    """Listar todos los partidos con filtros."""

    serializer_class = PartidoListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginacionEstandar
    filterset_class = PartidoFilter
    ordering_fields = ['fecha_hora', 'estado']

    def get_queryset(self):
        return Partido.objects.select_related(
            'fase', 'equipo_local', 'equipo_visitante'
        ).all()


@extend_schema(tags=['Partidos'])
class PartidoDetailView(generics.RetrieveAPIView):
    """Detalle de un partido."""

    serializer_class = PartidoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Partido.objects.select_related(
            'fase', 'fase__torneo', 'equipo_local', 'equipo_visitante'
        ).all()


@extend_schema_view(
    get=extend_schema(tags=['Partidos']),
)
class PartidosProximosView(generics.ListAPIView):
    """Listar próximos partidos (programados)."""

    serializer_class = PartidoListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginacionEstandar

    def get_queryset(self):
        return Partido.objects.select_related(
            'fase', 'equipo_local', 'equipo_visitante'
        ).filter(
            estado=Partido.Estado.PROGRAMADO,
            fecha_hora__gte=timezone.now(),
        ).order_by('fecha_hora')


@extend_schema_view(
    get=extend_schema(tags=['Partidos']),
)
class PartidosFinalizadosView(generics.ListAPIView):
    """Listar partidos finalizados."""

    serializer_class = PartidoListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginacionEstandar

    def get_queryset(self):
        return Partido.objects.select_related(
            'fase', 'equipo_local', 'equipo_visitante'
        ).filter(
            estado=Partido.Estado.FINALIZADO,
        ).order_by('-fecha_hora')
