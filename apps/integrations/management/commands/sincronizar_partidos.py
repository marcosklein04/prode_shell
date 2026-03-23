"""
Management command para sincronizar equipos y partidos desde la API externa.

Uso:
    python manage.py sincronizar_partidos
    python manage.py sincronizar_partidos --solo-equipos
    python manage.py sincronizar_partidos --solo-partidos
"""

from django.core.management.base import BaseCommand

from apps.integrations import services


class Command(BaseCommand):
    help = 'Sincroniza equipos y partidos desde la API de fútbol externa.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--solo-equipos',
            action='store_true',
            help='Sincronizar solo equipos',
        )
        parser.add_argument(
            '--solo-partidos',
            action='store_true',
            help='Sincronizar solo partidos',
        )

    def handle(self, *args, **options):
        solo_equipos = options['solo_equipos']
        solo_partidos = options['solo_partidos']

        if not solo_partidos:
            self.stdout.write('Sincronizando equipos...')
            try:
                cantidad = services.sincronizar_equipos()
                self.stdout.write(self.style.SUCCESS(f'Equipos sincronizados: {cantidad}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))
                if solo_equipos:
                    return

        if not solo_equipos:
            self.stdout.write('Sincronizando partidos...')
            try:
                cantidad = services.sincronizar_partidos()
                self.stdout.write(self.style.SUCCESS(f'Partidos sincronizados: {cantidad}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error: {e}'))
