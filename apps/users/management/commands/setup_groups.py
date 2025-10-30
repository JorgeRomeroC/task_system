from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from apps.users.models import User


class Command(BaseCommand):
    help = 'Configura los grupos de usuarios y crea usuarios de prueba'

    def handle(self, *args, **options):
        self.stdout.write('Configurando grupos...')
        
        # Crear o obtener grupos
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Grupo "Administrador" creado'))
        else:
            self.stdout.write('  Grupo "Administrador" ya existe')
        
        limited_group, created = Group.objects.get_or_create(name='Usuario Limitado')
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Grupo "Usuario Limitado" creado'))
        else:
            self.stdout.write('  Grupo "Usuario Limitado" ya existe')
        
        # Crear usuarios de prueba
        self.stdout.write('\nCreando usuarios de prueba...')
        
        # Usuario Administrador
        admin_email = 'admin@besimplit.com'
        if not User.objects.filter(email=admin_email).exists():
            admin_user = User.objects.create_user(
                email=admin_email,
                password='admin123'
            )
            admin_user.groups.add(admin_group)
            self.stdout.write(self.style.SUCCESS(f'✓ Usuario administrador creado: {admin_email}'))
        else:
            self.stdout.write(f'  Usuario {admin_email} ya existe')
        
        # Usuarios Limitados
        limited_users = [
            ('usuario1@besimplit.com', 'usuario123'),
            ('usuario2@besimplit.com', 'usuario123'),
        ]
        
        for email, password in limited_users:
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    password=password
                )
                user.groups.add(limited_group)
                self.stdout.write(self.style.SUCCESS(f'✓ Usuario limitado creado: {email}'))
            else:
                self.stdout.write(f'  Usuario {email} ya existe')
        
        self.stdout.write('\n' + self.style.SUCCESS('Configuración completada'))
        self.stdout.write('\nCredenciales de acceso:')
        self.stdout.write('  Administrador: admin@besimplit.com / admin123')
        self.stdout.write('  Usuario 1: usuario1@besimplit.com / usuario123')
        self.stdout.write('  Usuario 2: usuario2@besimplit.com / usuario123')