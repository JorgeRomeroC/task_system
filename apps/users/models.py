from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from apps.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):

     email = models.EmailField(max_length=255, unique=True)


     is_staff = models.BooleanField(
         'Es staff',
         default=False,
         help_text='Define si el usuario tiene acceso al administrador del sitio'
     )
     is_active = models.BooleanField(
         'Esta activo',
         default=True,
         help_text='Designa si este usuario debe ser tratado como activo.'
     )
     date_joined = models.DateTimeField('Fecha de registro', auto_now_add=True)
     updated_at = models.DateTimeField('Última actualización', auto_now=True)

     objects = UserManager()

     USERNAME_FIELD = 'email'
     REQUIRED_FIELDS = []

     class Meta:
         verbose_name = 'Usuario'
         verbose_name_plural = 'Usuarios'
         ordering = ['-date_joined']
         indexes = [
             models.Index(fields=['email']),
             models.Index(fields=['is_active']),
         ]

     def __str__(self):
         return self.email

