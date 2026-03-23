"""
Management command para sincronizar resultados y recalcular puntos.

Uso:
    python manage.py sincronizar_resultados

Ideal para ejecutar con cron cada 5-10 minutos durante partidos.
"""

from django.core.management.base import BaseCommand

from apps.integrations import services


class Command(BaseCommand):
    help = 'Sincroniza resultados de partidos y recalcula puntajes.'

    def handle(self, *args, **options):
        self.stdout.write('Sincronizando resultados...')
        try:
            resultado = services.sincronizar_resultados()
            self.stdout.write(self.style.SUCCESS(
                f'Procesados: {resultado["procesados"]}, '
                f'Finalizados: {resultado["partidos_finalizados"]}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
