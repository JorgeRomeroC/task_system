from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count
from django.contrib import messages
from .models import Task
from apps.users.models import User


def is_admin_or_superuser(user):
    """Verifica si el usuario es administrador o superusuario."""
    return user.is_superuser or user.groups.filter(name='Administrador').exists()


@login_required
@user_passes_test(is_admin_or_superuser, login_url='tasks:task_list')
def dashboard(request):
    """Dashboard con gestión completa de tareas. Solo admin/superuser."""
    
    # Obtener todas las tareas
    tasks = Task.objects.select_related('assigned_to', 'created_by').all()
    
    # Aplicar filtros
    search = request.GET.get('search', '')
    filter_status = request.GET.get('filter', 'all')
    filter_user = request.GET.get('user', '')
    
    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(assigned_to__email__icontains=search)
        )
    
    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)
    
    if filter_user:
        tasks = tasks.filter(assigned_to_id=filter_user)
    
    # Estadísticas generales
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    pending_tasks = Task.objects.filter(completed=False).count()
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Estadísticas por usuario
    user_stats = User.objects.filter(
        groups__name='Usuario Limitado'
    ).annotate(
        total=Count('assigned_tasks'),
        completed=Count('assigned_tasks', filter=Q(assigned_tasks__completed=True))
    ).order_by('-total')
    
    # Lista de usuarios para asignar
    users_list = User.objects.filter(groups__name='Usuario Limitado')
    
    context = {
        'tasks': tasks,
        'search': search,
        'filter_status': filter_status,
        'filter_user': filter_user,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_rate': completion_rate,
        'user_stats': user_stats,
        'users_list': users_list,
        'is_dashboard': True,
    }
    
    return render(request, 'tasks/dashboard.html', context)


@login_required
@user_passes_test(is_admin_or_superuser, login_url='tasks:task_list')
@require_http_methods(["POST"])
def dashboard_task_create(request):
    """Crea una nueva tarea desde el dashboard (HTMX)."""
    try:
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        assigned_to_id = request.POST.get('assigned_to', '').strip()

        if not title or len(title) < 3:
            return HttpResponse(
                '<div class="text-red-500 text-sm mt-2">El título debe tener al menos 3 caracteres</div>',
                status=400
            )

        assigned_user = None
        if assigned_to_id:
            try:
                assigned_user = User.objects.get(id=assigned_to_id, groups__name='Usuario Limitado')
            except User.DoesNotExist:
                return HttpResponse(
                    '<div class="text-red-500 text-sm mt-2">Usuario no válido</div>',
                    status=400
                )

        task = Task.objects.create(
            title=title,
            description=description,
            assigned_to=assigned_user,
            created_by=request.user
        )

        context = {
            'task': task,
            'is_dashboard': True,
        }
        
        response = render(request, 'tasks/partials/dashboard_task_item.html', context)
        response['HX-Trigger'] = 'taskCreated'
        return response
    
    except Exception:
        return HttpResponse(
            '<div class="text-red-500 text-sm mt-2">Error al crear la tarea</div>',
            status=500
        )


@login_required
@user_passes_test(is_admin_or_superuser, login_url='tasks:task_list')
@require_http_methods(["GET"])
def dashboard_task_detail(request, pk):
    """Obtiene el detalle de una tarea para edición desde dashboard (HTMX)."""
    try:
        task = get_object_or_404(Task, pk=pk)
        users_list = User.objects.filter(groups__name='Usuario Limitado')
        
        context = {
            'task': task,
            'users_list': users_list,
            'is_dashboard': True,
        }
        return render(request, 'tasks/partials/dashboard_task_edit_form.html', context)
    
    except Exception:
        return HttpResponse(
            '<div class="text-red-500 text-sm mt-2">Error al cargar la tarea</div>',
            status=500
        )


@login_required
@user_passes_test(is_admin_or_superuser, login_url='tasks:task_list')
@require_http_methods(["POST"])
def dashboard_task_update(request, pk):
    """Actualiza una tarea desde el dashboard (HTMX)."""
    try:
        task = get_object_or_404(Task, pk=pk)

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        assigned_to_id = request.POST.get('assigned_to', '').strip()

        if not title or len(title) < 3:
            return HttpResponse(
                '<div class="text-red-500 text-sm mt-2">El título debe tener al menos 3 caracteres</div>',
                status=400
            )

        task.title = title
        task.description = description
        
        if assigned_to_id:
            try:
                task.assigned_to = User.objects.get(id=assigned_to_id, groups__name='Usuario Limitado')
            except User.DoesNotExist:
                pass
        else:
            task.assigned_to = None

        task.save()

        context = {
            'task': task,
            'is_dashboard': True,
        }
        
        response = render(request, 'tasks/partials/dashboard_task_item.html', context)
        response['HX-Trigger'] = 'taskUpdated'
        return response
    
    except Exception:
        return HttpResponse(
            '<div class="text-red-500 text-sm mt-2">Error al actualizar la tarea</div>',
            status=500
        )


@login_required
@user_passes_test(is_admin_or_superuser, login_url='tasks:task_list')
@require_http_methods(["POST"])
def dashboard_task_toggle(request, pk):
    """Alterna el estado completado de una tarea desde dashboard (HTMX)."""
    try:
        task = get_object_or_404(Task, pk=pk)
        task.toggle_completed()

        context = {
            'task': task,
            'is_dashboard': True,
        }
        
        response = render(request, 'tasks/partials/dashboard_task_item.html', context)
        response['HX-Trigger'] = f'taskToggled:{{"completed": {str(task.completed).lower()}}}'
        return response
    
    except Exception:
        return HttpResponse(status=500)


@login_required
@user_passes_test(is_admin_or_superuser, login_url='tasks:task_list')
@require_http_methods(["DELETE"])
def dashboard_task_delete(request, pk):
    """Elimina una tarea desde el dashboard (HTMX)."""
    try:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        
        response = HttpResponse('')
        response['HX-Trigger'] = 'taskDeleted'
        return response
    except Exception:
        return HttpResponse(status=500)
