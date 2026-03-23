"""Configuración de URLs principal del proyecto."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/matches/', include('apps.matches.urls')),
    path('api/predictions/', include('apps.predictions.urls')),
    path('api/rankings/', include('apps.rankings.urls')),
    path('api/spaces/', include('apps.spaces.urls')),
    path('api/admin/', include('apps.integrations.urls')),

    # Documentación API (Swagger / ReDoc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Título del admin
admin.site.site_header = 'Prode Shell - Administración'
admin.site.site_title = 'Prode Shell'
admin.site.index_title = 'Panel de administración'
