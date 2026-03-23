"""URLs administrativas (prefijo: /api/admin/)."""

from django.urls import path

from apps.predictions.views import AdminPronosticosView
from apps.rankings.views import AdminRecalcularPuntosView
from apps.users.views import AdminUsuariosListView

from . import views

app_name = 'admin_api'

urlpatterns = [
    # Sincronización
    path('sync/matches/', views.SincronizarPartidosView.as_view(), name='sync-matches'),
    path('sync/results/', views.SincronizarResultadosView.as_view(), name='sync-results'),
    path('sync/logs/', views.LogsSincronizacionView.as_view(), name='sync-logs'),

    # Recálculo
    path('recalculate/scores/', AdminRecalcularPuntosView.as_view(), name='recalculate-scores'),

    # Consultas admin
    path('users/', AdminUsuariosListView.as_view(), name='users-list'),
    path('predictions/', AdminPronosticosView.as_view(), name='predictions-list'),
]
