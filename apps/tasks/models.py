from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.mail import send_mail


class Task(models.Model):

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(3)],
        verbose_name='Título',
        help_text='Título de la tarea (mínimo 3 caracteres)'
    )

    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada de la tarea',
        blank=True,
        default=''
    )

    completed = models.BooleanField(
        default=False,
        verbose_name='Completada',
        help_text='Indica si la tarea está completada'
    )
    
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name='Asignado a',
        help_text='Usuario al que se le asignó esta tarea'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_tasks',
        verbose_name='Creado por',
        help_text='Usuario que creó esta tarea'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación',
        help_text='Fecha y hora de creación de la tarea'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización',
        help_text='Fecha y hora de la última actualización'
    )

    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at'], name='task_created_idx'),
            models.Index(fields=['completed'], name='task_completed_idx'),
            models.Index(fields=['assigned_to'], name='task_assigned_idx'),
        ]

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.title}"

    def toggle_completed(self):
        """Cambia el estado de completado de la tarea y envía email al administrador."""
        was_completed = self.completed
        self.completed = not self.completed
        self.save(update_fields=['completed', 'updated_at'])
        
        # Enviar email solo si la tarea pasó de pendiente a completada
        if not was_completed and self.completed:
            self.send_completion_email()
        
        return self.completed

    def send_completion_email(self):
        """Envía email al administrador cuando se completa una tarea."""
        try:
            if self.created_by and self.assigned_to:
                subject = f'Tarea completada: {self.title}'
                message = f'''
Tarea completada exitosamente.

Detalles:
- Tarea: {self.title}
- Completada por: {self.assigned_to.email}
- Fecha de completación: {self.updated_at.strftime("%d/%m/%Y %H:%M")}
- Descripción: {self.description or "Sin descripción"}
'''
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[self.created_by.email],
                    fail_silently=True,
                )
        except Exception:
            pass