"""Vistas administrativas para sincronización."""

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.views import AdminUsuariosListView
from core.pagination import PaginacionEstandar
from core.permissions import EsAdmin

from . import services
from .models import LogSincronizacion
from .serializers import LogSincronizacionSerializer


@extend_schema(tags=['Admin'])
class SincronizarPartidosView(APIView):
    """Sincronizar equipos y partidos desde la API externa."""

    permission_classes = [IsAuthenticated, EsAdmin]

    def post(self, request):
        try:
            equipos = services.sincronizar_equipos()
            partidos = services.sincronizar_partidos()
            return Response({
                'mensaje': 'Sincronización completada.',
                'equipos_sincronizados': equipos,
                'partidos_sincronizados': partidos,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'Error en la sincronización: {str(e)}',
            }, status=status.HTTP_502_BAD_GATEWAY)


@extend_schema(tags=['Admin'])
class SincronizarResultadosView(APIView):
    """Sincronizar resultados y recalcular puntos."""

    permission_classes = [IsAuthenticated, EsAdmin]

    def post(self, request):
        try:
            resultado = services.sincronizar_resultados()
            return Response({
                'mensaje': 'Resultados sincronizados.',
                **resultado,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'Error sincronizando resultados: {str(e)}',
            }, status=status.HTTP_502_BAD_GATEWAY)


@extend_schema_view(
    get=extend_schema(tags=['Admin']),
)
class LogsSincronizacionView(generics.ListAPIView):
    """Listar logs de sincronización."""

    serializer_class = LogSincronizacionSerializer
    permission_classes = [IsAuthenticated, EsAdmin]
    pagination_class = PaginacionEstandar
    queryset = LogSincronizacion.objects.all()
    filterset_fields = ['proveedor', 'tipo_entidad', 'estado']
