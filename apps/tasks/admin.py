from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'completed', 'created_at', 'updated_at']
    list_filter = ['completed', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['completed']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Información Principal', {
            'fields': ('title', 'description')
        }),
        ('Estado', {
            'fields': ('completed',)
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related()