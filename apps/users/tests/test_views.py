"""Tests para vistas de autenticación."""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

Usuario = get_user_model()


@pytest.mark.django_db
class TestRegistro:
    url = reverse('users:register')

    def test_registro_exitoso(self, api_client):
        data = {
            'email': 'nuevo@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
        }
        response = api_client.post(self.url, data)
        assert response.status_code == 201
        assert response.data['usuario']['email'] == 'nuevo@test.com'
        assert Usuario.objects.filter(email='nuevo@test.com').exists()

    def test_registro_passwords_no_coinciden(self, api_client):
        data = {
            'email': 'nuevo@test.com',
            'first_name': 'Nuevo',
            'last_name': 'Usuario',
            'password': 'SecurePass123!',
            'password_confirm': 'OtraPass456!',
        }
        response = api_client.post(self.url, data)
        assert response.status_code == 400

    def test_registro_email_duplicado(self, api_client, usuario):
        data = {
            'email': 'usuario@test.com',
            'first_name': 'Otro',
            'last_name': 'Usuario',
            'password': 'SecurePass123!',
            'password_confirm': 'SecurePass123!',
        }
        response = api_client.post(self.url, data)
        assert response.status_code == 400


@pytest.mark.django_db
class TestLogin:
    url = reverse('users:login')

    def test_login_exitoso(self, api_client, usuario):
        data = {'email': 'usuario@test.com', 'password': 'TestPass123!'}
        response = api_client.post(self.url, data)
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_credenciales_invalidas(self, api_client, usuario):
        data = {'email': 'usuario@test.com', 'password': 'wrongpassword'}
        response = api_client.post(self.url, data)
        assert response.status_code == 401


@pytest.mark.django_db
class TestMe:
    url = reverse('users:me')

    def test_me_autenticado(self, api_client_autenticado, usuario):
        response = api_client_autenticado.get(self.url)
        assert response.status_code == 200
        assert response.data['email'] == usuario.email

    def test_me_no_autenticado(self, api_client):
        response = api_client.get(self.url)
        assert response.status_code == 401
