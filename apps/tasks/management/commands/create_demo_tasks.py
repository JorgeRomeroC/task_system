from django.core.management.base import BaseCommand
from apps.tasks.models import Task
import random


class Command(BaseCommand):
    help = 'Crea datos de demostración para el sistema de tareas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todas las tareas existentes antes de crear las nuevas',
        )
        parser.add_argument(
            '--count',
            type=int,
            default=15,
            help='Número de tareas a crear (default: 15)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            count = Task.objects.count()
            Task.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f'Se eliminaron {count} tareas existentes')
            )

        count = options['count']

        # Datos de ejemplo
        tasks_data = [
            {
                'title': 'Implementar autenticación de usuarios',
                'description': 'Configurar sistema de login/logout con Django Authentication. Incluir validación de credenciales y manejo de sesiones.',
                'completed': True
            },
            {
                'title': 'Diseñar base de datos',
                'description': 'Crear diagrama ER y definir modelos para el sistema. Considerar relaciones y optimizaciones necesarias.',
                'completed': True
            },
            {
                'title': 'Configurar entorno de desarrollo',
                'description': 'Instalar dependencias, configurar virtual environment y variables de entorno.',
                'completed': True
            },
            {
                'title': 'Desarrollar API REST con DRF',
                'description': 'Crear endpoints para CRUD de tareas utilizando Django Rest Framework. Incluir serializers y viewsets.',
                'completed': False
            },
            {
                'title': 'Integrar HTMX en el frontend',
                'description': 'Implementar interacciones dinámicas sin recargar página usando HTMX para crear, editar y eliminar tareas.',
                'completed': False
            },
            {
                'title': 'Aplicar estilos con Tailwind CSS',
                'description': 'Diseñar interfaz moderna y responsive utilizando las utility classes de Tailwind CSS.',
                'completed': False
            },
            {
                'title': 'Escribir tests unitarios',
                'description': 'Crear tests para modelos, vistas y API endpoints. Asegurar cobertura mínima del 80%.',
                'completed': False
            },
            {
                'title': 'Optimizar consultas a la base de datos',
                'description': 'Analizar queries con Django Debug Toolbar y aplicar select_related y prefetch_related donde sea necesario.',
                'completed': False
            },
            {
                'title': 'Documentar API con Swagger',
                'description': 'Integrar drf-yasg para generar documentación automática de la API REST.',
                'completed': False
            },
            {
                'title': 'Implementar sistema de filtros',
                'description': 'Agregar filtros por estado (completadas/pendientes) y búsqueda por texto en tareas.',
                'completed': False
            },
            {
                'title': 'Configurar CI/CD pipeline',
                'description': 'Setup de GitHub Actions para ejecutar tests automáticamente en cada push.',
                'completed': False
            },
            {
                'title': 'Crear dashboard de estadísticas',
                'description': 'Desarrollar página con métricas: total de tareas, completadas, pendientes y gráficos de progreso.',
                'completed': False
            },
            {
                'title': 'Implementar exportación de reportes',
                'description': 'Agregar funcionalidad para exportar tareas en formato CSV y PDF.',
                'completed': False
            },
            {
                'title': 'Añadir animaciones y transiciones',
                'description': 'Mejorar UX con animaciones suaves usando Tailwind transitions y transforms.',
                'completed': False
            },
            {
                'title': 'Revisar código y refactorizar',
                'description': 'Hacer code review, eliminar código duplicado y mejorar la estructura siguiendo buenas prácticas.',
                'completed': False
            },
            {
                'title': 'Preparar presentación del proyecto',
                'description': 'Crear documentación README completa con instrucciones de instalación y decisiones técnicas.',
                'completed': False
            },
        ]

        # Crear tareas
        created_count = 0
        for i in range(min(count, len(tasks_data))):
            task_data = tasks_data[i]
            task = Task.objects.create(**task_data)
            created_count += 1

            status = "✓" if task.completed else "○"
            self.stdout.write(
                self.style.SUCCESS(f'{status} Tarea creada: {task.title}')
            )

        # Si se solicitan más tareas de las que hay en la lista, crear genéricas
        if count > len(tasks_data):
            for i in range(count - len(tasks_data)):
                task = Task.objects.create(
                    title=f'Tarea de ejemplo #{i + len(tasks_data) + 1}',
                    description=f'Esta es una tarea de demostración generada automáticamente.',
                    completed=random.choice([True, False])
                )
                created_count += 1
                status = "✓" if task.completed else "○"
                self.stdout.write(
                    self.style.SUCCESS(f'{status} Tarea creada: {task.title}')
                )

        # Estadísticas finales
        total = Task.objects.count()
        completed = Task.objects.filter(completed=True).count()
        pending = Task.objects.filter(completed=False).count()

        self.stdout.write(self.style.SUCCESS('\n' + '=' * 50))
        self.stdout.write(
            self.style.SUCCESS(f'✓ Se crearon {created_count} tareas de demostración')
        )
        self.stdout.write(self.style.SUCCESS(f'Total de tareas: {total}'))
        self.stdout.write(self.style.SUCCESS(f'Completadas: {completed}'))
        self.stdout.write(self.style.SUCCESS(f'Pendientes: {pending}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))