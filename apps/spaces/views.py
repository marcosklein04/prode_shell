"""Vistas para salas/espacios."""

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import PaginacionEstandar

from . import services
from .models import MiembroSala, Sala
from .serializers import (
    ExpulsarMiembroSerializer,
    MiembroSalaSerializer,
    RankingSalaSerializer,
    SalaCreateSerializer,
    SalaListSerializer,
    SalaSerializer,
    UnirseSalaSerializer,
)

Usuario = get_user_model()


@extend_schema(tags=['Salas'])
class SalaCreateView(generics.CreateAPIView):
    """Crear una nueva sala."""

    serializer_class = SalaCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sala = services.crear_sala(
            usuario=request.user,
            **serializer.validated_data,
        )

        return Response(
            SalaSerializer(sala, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema_view(
    get=extend_schema(tags=['Salas']),
)
class MisSalasView(generics.ListAPIView):
    """Listar las salas del usuario autenticado."""

    serializer_class = SalaListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginacionEstandar

    def get_queryset(self):
        return Sala.objects.filter(
            miembros__usuario=self.request.user,
            activa=True,
        ).select_related('creador')


@extend_schema_view(
    get=extend_schema(tags=['Salas']),
)
class SalasPublicasView(generics.ListAPIView):
    """Listar salas públicas disponibles."""

    serializer_class = SalaListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginacionEstandar
    search_fields = ['nombre']

    def get_queryset(self):
        return Sala.objects.filter(
            es_publica=True,
            activa=True,
        ).select_related('creador')


@extend_schema(tags=['Salas'])
class SalaDetailView(generics.RetrieveAPIView):
    """Detalle de una sala (solo para miembros)."""

    serializer_class = SalaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Sala.objects.filter(
            miembros__usuario=self.request.user,
        ).select_related('creador')


@extend_schema(tags=['Salas'])
class UnirseSalaView(APIView):
    """Unirse a una sala usando código de invitación."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UnirseSalaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sala = services.unirse_a_sala(
            usuario=request.user,
            codigo=serializer.validated_data['codigo'],
        )

        return Response(
            {
                'mensaje': f'Te uniste a la sala "{sala.nombre}".',
                'sala': SalaSerializer(sala, context={'request': request}).data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(tags=['Salas'])
class SalirSalaView(APIView):
    """Abandonar una sala."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        sala = get_object_or_404(Sala, pk=pk)
        services.salir_de_sala(request.user, sala)
        return Response(
            {'mensaje': f'Abandonaste la sala "{sala.nombre}".'},
            status=status.HTTP_200_OK,
        )


@extend_schema_view(
    get=extend_schema(tags=['Salas']),
)
class MiembrosSalaView(generics.ListAPIView):
    """Listar miembros de una sala."""

    serializer_class = MiembroSalaSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PaginacionEstandar

    def get_queryset(self):
        sala_id = self.kwargs['pk']
        # Verificar que el usuario es miembro
        get_object_or_404(MiembroSala, sala_id=sala_id, usuario=self.request.user)
        return MiembroSala.objects.filter(
            sala_id=sala_id
        ).select_related('usuario').order_by('-usuario__puntos_totales')


@extend_schema(tags=['Salas'])
class RankingSalaView(APIView):
    """Ranking de una sala específica."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        sala = get_object_or_404(Sala, pk=pk)
        # Verificar que el usuario es miembro
        get_object_or_404(MiembroSala, sala=sala, usuario=request.user)

        paginator = PaginacionEstandar()
        usuarios = services.obtener_ranking_sala(sala)

        page = paginator.paginate_queryset(usuarios, request)

        offset = paginator.page.start_index()
        for i, usuario in enumerate(page):
            usuario._posicion = offset + i

        serializer = RankingSalaSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


@extend_schema(tags=['Salas'])
class ExpulsarMiembroView(APIView):
    """Expulsar a un miembro de la sala (solo admin de sala)."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        sala = get_object_or_404(Sala, pk=pk)
        serializer = ExpulsarMiembroSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario_a_expulsar = get_object_or_404(
            Usuario, id=serializer.validated_data['usuario_id']
        )
        services.expulsar_miembro(sala, request.user, usuario_a_expulsar)

        return Response(
            {'mensaje': f'Usuario expulsado de la sala.'},
            status=status.HTTP_200_OK,
        )
