from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'get_groups']
    filter_horizontal = ('groups',)
    exclude = ('user_permissions',)
    readonly_fields = ('date_joined', 'last_login')

    # Campos al crear nuevo usuario
    add_fieldsets = (
        ('Permisos y Acceso', {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
            'description': 'Selecciona el grupo apropiado según el rol del usuario.'
        }),
    )

    def get_groups(self, obj):
        """Muestra los grupos del usuario en la lista"""
        return ", ".join([group.name for group in obj.groups.all()]) or "Sin grupo"

    get_groups.short_description = 'Grupos'
