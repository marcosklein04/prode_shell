"""Utilidades compartidas."""

from django.utils import timezone


def ahora():
    """Retorna datetime actual con timezone."""
    return timezone.now()
