"""URLs de autenticación y usuarios."""

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegistroView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('refresh/', views.RefreshTokenView.as_view(), name='refresh'),
    path('me/', views.MeView.as_view(), name='me'),
]
