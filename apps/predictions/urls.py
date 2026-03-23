"""URLs de pronósticos."""

from django.urls import path

from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.PronosticoCreateView.as_view(), name='create'),
    path('<int:pk>/', views.PronosticoUpdateView.as_view(), name='update'),
    path('me/', views.MisPronosticosView.as_view(), name='my-list'),
    path('me/<int:match_id>/', views.MiPronosticoPartidoView.as_view(), name='my-match'),
]
