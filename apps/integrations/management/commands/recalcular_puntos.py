"""
Management command para recalcular todos los puntajes.

Uso:
    python manage.py recalcular_puntos
"""

from django.core.management.base import BaseCommand

from apps.rankings import services as ranking_services


class Command(BaseCommand):
    help = 'Recalcula todos los puntajes de pronósticos y totales de usuarios.'

    def handle(self, *args, **options):
        self.stdout.write('Recalculando puntajes...')
        try:
            total = ranking_services.recalcular_todos_los_puntos()
            self.stdout.write(self.style.SUCCESS(
                f'Pronósticos actualizados: {total}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
