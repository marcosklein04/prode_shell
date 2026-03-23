"""URLs de partidos."""

from django.urls import path

from . import views

app_name = 'matches'

urlpatterns = [
    path('', views.PartidoListView.as_view(), name='list'),
    path('upcoming/', views.PartidosProximosView.as_view(), name='upcoming'),
    path('finished/', views.PartidosFinalizadosView.as_view(), name='finished'),
    path('<int:pk>/', views.PartidoDetailView.as_view(), name='detail'),
]
