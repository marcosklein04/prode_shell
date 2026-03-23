"""Vistas de autenticación y usuarios."""

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.pagination import PaginacionEstandar
from core.permissions import EsAdmin

from .serializers import RegistroSerializer, UsuarioAdminSerializer, UsuarioSerializer

Usuario = get_user_model()


@extend_schema(tags=['Auth'])
class RegistroView(generics.CreateAPIView):
    """Registro de nuevo usuario."""

    serializer_class = RegistroSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        return Response(
            {
                'mensaje': 'Usuario registrado correctamente.',
                'usuario': UsuarioSerializer(usuario).data,
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=['Auth'])
class LoginView(TokenObtainPairView):
    """Login con email y contraseña. Retorna access y refresh tokens."""

    permission_classes = [AllowAny]


@extend_schema(tags=['Auth'])
class RefreshTokenView(TokenRefreshView):
    """Refrescar access token usando el refresh token."""

    permission_classes = [AllowAny]


@extend_schema(tags=['Auth'])
class MeView(generics.RetrieveUpdateAPIView):
    """Obtener o actualizar el perfil del usuario autenticado."""

    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema_view(
    get=extend_schema(tags=['Admin']),
)
class AdminUsuariosListView(generics.ListAPIView):
    """Listar todos los usuarios (solo admin)."""

    serializer_class = UsuarioAdminSerializer
    permission_classes = [IsAuthenticated, EsAdmin]
    pagination_class = PaginacionEstandar
    queryset = Usuario.objects.all()
    filterset_fields = ['rol', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['puntos_totales', 'date_joined', 'last_name']
