from django.db import models
from django.core.validators import MinLengthValidator


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
        ]

    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"{status} {self.title}"

    def toggle_completed(self):
        """Cambia el estado de completado de la tarea."""
        self.completed = not self.completed
        self.save(update_fields=['completed', 'updated_at'])
        return self.completed