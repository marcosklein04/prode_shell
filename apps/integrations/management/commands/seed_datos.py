"""
Management command para cargar datos de prueba (seed).

Uso:
    python manage.py seed_datos
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.matches.models import Partido
from apps.rankings.models import ReglaPuntaje
from apps.tournaments.models import Equipo, Fase, Torneo

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Carga datos de prueba para desarrollo.'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos de prueba...')

        # Admin
        admin, created = Usuario.objects.get_or_create(
            email='admin@shell.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'Shell',
                'rol': 'admin',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            admin.set_password('Admin123!')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin creado: admin@shell.com / Admin123!'))

        # Usuarios de prueba
        usuarios_data = [
            ('juan@test.com', 'Juan', 'Pérez'),
            ('maria@test.com', 'María', 'González'),
            ('carlos@test.com', 'Carlos', 'López'),
            ('ana@test.com', 'Ana', 'Martínez'),
            ('pedro@test.com', 'Pedro', 'Rodríguez'),
        ]
        for email, nombre, apellido in usuarios_data:
            user, created = Usuario.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': nombre,
                    'last_name': apellido,
                },
            )
            if created:
                user.set_password('Test1234!')
                user.save()

        self.stdout.write(self.style.SUCCESS(f'Usuarios creados: {len(usuarios_data)}'))

        # Torneo
        torneo, _ = Torneo.objects.get_or_create(
            nombre='Copa Mundial FIFA 2026',
            temporada=2026,
            defaults={'activo': True, 'api_externa_id': 1},
        )

        # Fases
        fases_data = [
            ('Fase de grupos', 1),
            ('Octavos de final', 2),
            ('Cuartos de final', 3),
            ('Semifinales', 4),
            ('Tercer puesto', 5),
            ('Final', 6),
        ]
        fases = {}
        for nombre, orden in fases_data:
            fase, _ = Fase.objects.get_or_create(
                torneo=torneo,
                nombre=nombre,
                defaults={'orden': orden},
            )
            fases[nombre] = fase

        # Equipos
        equipos_data = [
            ('Argentina', 'ARG', 1),
            ('Brasil', 'BRA', 2),
            ('Alemania', 'GER', 3),
            ('Francia', 'FRA', 4),
            ('España', 'ESP', 5),
            ('Inglaterra', 'ENG', 6),
            ('Países Bajos', 'NED', 7),
            ('Portugal', 'POR', 8),
            ('México', 'MEX', 9),
            ('Estados Unidos', 'USA', 10),
            ('Canadá', 'CAN', 11),
            ('Uruguay', 'URU', 12),
            ('Colombia', 'COL', 13),
            ('Japón', 'JPN', 14),
            ('Corea del Sur', 'KOR', 15),
            ('Australia', 'AUS', 16),
        ]
        equipos = {}
        for nombre, codigo, api_id in equipos_data:
            equipo, _ = Equipo.objects.get_or_create(
                api_externa_id=api_id,
                defaults={'nombre': nombre, 'codigo': codigo},
            )
            equipos[codigo] = equipo

        self.stdout.write(self.style.SUCCESS(f'Equipos creados: {len(equipos_data)}'))

        # Partidos de ejemplo
        ahora = timezone.now()
        partidos_data = [
            # Partidos pasados (finalizados)
            (equipos['ARG'], equipos['MEX'], -5, 'finalizado', 2, 0),
            (equipos['BRA'], equipos['KOR'], -4, 'finalizado', 1, 1),
            (equipos['FRA'], equipos['AUS'], -3, 'finalizado', 3, 1),
            (equipos['ESP'], equipos['JPN'], -2, 'finalizado', 0, 2),
            # Partidos futuros (programados)
            (equipos['ARG'], equipos['BRA'], 3, 'programado', None, None),
            (equipos['FRA'], equipos['ESP'], 4, 'programado', None, None),
            (equipos['GER'], equipos['ENG'], 5, 'programado', None, None),
            (equipos['NED'], equipos['POR'], 6, 'programado', None, None),
            (equipos['USA'], equipos['URU'], 7, 'programado', None, None),
            (equipos['COL'], equipos['CAN'], 8, 'programado', None, None),
        ]

        fase_grupos = fases['Fase de grupos']
        for local, visitante, dias, estado, gl, gv in partidos_data:
            Partido.objects.get_or_create(
                equipo_local=local,
                equipo_visitante=visitante,
                fase=fase_grupos,
                defaults={
                    'fecha_hora': ahora + timezone.timedelta(days=dias),
                    'estado': estado,
                    'goles_local': gl,
                    'goles_visitante': gv,
                },
            )

        self.stdout.write(self.style.SUCCESS(f'Partidos creados: {len(partidos_data)}'))

        # Reglas de puntaje
        ReglaPuntaje.objects.get_or_create(
            torneo=torneo,
            tipo=ReglaPuntaje.TipoRegla.RESULTADO_EXACTO,
            defaults={'puntos': 3, 'descripcion': 'Acertar el resultado exacto'},
        )
        ReglaPuntaje.objects.get_or_create(
            torneo=torneo,
            tipo=ReglaPuntaje.TipoRegla.ACIERTO_GANADOR,
            defaults={'puntos': 1, 'descripcion': 'Acertar ganador o empate'},
        )

        self.stdout.write(self.style.SUCCESS('Reglas de puntaje creadas'))
        self.stdout.write(self.style.SUCCESS('¡Seed completado!'))
