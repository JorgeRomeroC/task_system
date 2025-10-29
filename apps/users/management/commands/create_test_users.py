# Crear este archivo en: apps/users/management/commands/create_test_users.py

from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    help = 'Crea usuarios de prueba para el desarrollo'

    def handle(self, *args, **kwargs):
        # Crear superusuario
        if not User.objects.filter(email='admin@test.com').exists():
            User.objects.create_superuser(
                email='admin@test.com',
                password='admin123'
            )
            self.stdout.write(
                self.style.SUCCESS('Superusuario creado: admin@test.com / admin123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('El superusuario ya existe')
            )

        # Crear usuario regular
        if not User.objects.filter(email='user@test.com').exists():
            User.objects.create_user(
                email='user@test.com',
                password='user123'
            )
            self.stdout.write(
                self.style.SUCCESS('Usuario regular creado: user@test.com / user123')
            )
        else:
            self.stdout.write(
                self.style.WARNING('El usuario regular ya existe')
            )