"""Modelo de usuario personalizado."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    """Manager personalizado para Usuario con email como identificador."""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio.')
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        usuario = self.model(email=email, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', Usuario.Rol.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    """Modelo de usuario personalizado con email como campo principal."""

    class Rol(models.TextChoices):
        USER = 'user', 'Usuario'
        ADMIN = 'admin', 'Administrador'

    # Remover username, usar email
    username = None
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Nombre', max_length=150)
    last_name = models.CharField('Apellido', max_length=150)
    rol = models.CharField(
        'Rol',
        max_length=10,
        choices=Rol.choices,
        default=Rol.USER,
    )
    puntos_totales = models.IntegerField('Puntos totales', default=0, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UsuarioManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-puntos_totales']
        indexes = [
            models.Index(fields=['-puntos_totales'], name='idx_puntos_totales'),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    @property
    def es_admin(self):
        return self.rol == self.Rol.ADMIN or self.is_superuser

    @property
    def nombre_completo(self):
        return f'{self.first_name} {self.last_name}'
