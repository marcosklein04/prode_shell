"""URLs de salas/espacios."""

from django.urls import path

from . import views

app_name = 'spaces'

urlpatterns = [
    path('', views.SalaCreateView.as_view(), name='create'),
    path('me/', views.MisSalasView.as_view(), name='my-list'),
    path('public/', views.SalasPublicasView.as_view(), name='public-list'),
    path('join/', views.UnirseSalaView.as_view(), name='join'),
    path('<int:pk>/', views.SalaDetailView.as_view(), name='detail'),
    path('<int:pk>/leave/', views.SalirSalaView.as_view(), name='leave'),
    path('<int:pk>/members/', views.MiembrosSalaView.as_view(), name='members'),
    path('<int:pk>/ranking/', views.RankingSalaView.as_view(), name='ranking'),
    path('<int:pk>/kick/', views.ExpulsarMiembroView.as_view(), name='kick'),
]
