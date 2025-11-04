from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'assigned_to', 'created_by', 'created_at')
    list_filter = ('completed', 'created_at', 'assigned_to')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información de la Tarea', {
            'fields': ('title', 'description', 'completed')
        }),
        ('Asignación', {
            'fields': ('assigned_to', 'created_by')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es una nueva tarea
            if not obj.created_by:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)