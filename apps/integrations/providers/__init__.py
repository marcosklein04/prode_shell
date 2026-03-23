"""Proveedores de datos de fútbol."""

from .api_football import ApiFootballProvider
from .base import BaseFootballProvider

__all__ = ['BaseFootballProvider', 'ApiFootballProvider']
