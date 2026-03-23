"""Vistas para rankings."""

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import PaginacionEstandar
from core.permissions import EsAdmin

from . import services
from .serializers import MiRankingSerializer, RankingSerializer


@extend_schema_view(
    get=extend_schema(tags=['Rankings']),
)
class RankingListView(APIView):
    """Ranking global de usuarios."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        paginator = PaginacionEstandar()
        usuarios = services.obtener_ranking()

        page = paginator.paginate_queryset(usuarios, request)

        # Asignar posición basada en el offset de la paginación
        offset = paginator.page.start_index()
        for i, usuario in enumerate(page):
            usuario._posicion = offset + i

        serializer = RankingSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


@extend_schema(tags=['Rankings'])
class MiRankingView(APIView):
    """Posición del usuario actual en el ranking."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = services.obtener_posicion_usuario(request.user)
        serializer = MiRankingSerializer(data)
        return Response(serializer.data)


@extend_schema(tags=['Admin'])
class AdminRecalcularPuntosView(APIView):
    """Recalcular todos los puntajes (solo admin)."""

    permission_classes = [IsAuthenticated, EsAdmin]

    def post(self, request):
        total = services.recalcular_todos_los_puntos()
        return Response({
            'mensaje': 'Puntajes recalculados correctamente.',
            'pronosticos_actualizados': total,
        }, status=status.HTTP_200_OK)
