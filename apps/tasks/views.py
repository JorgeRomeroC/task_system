from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib import messages
from .models import Task
from apps.users.models import User


def is_admin(user):
    """Verifica si el usuario pertenece al grupo Administrador."""
    return user.groups.filter(name='Administrador').exists()


@login_required
def task_list(request):
    """Vista principal que renderiza la lista de tareas."""
    user = request.user
    is_user_admin = is_admin(user)
    
    # Usuarios limitados solo ven sus tareas asignadas
    if is_user_admin:
        tasks = Task.objects.all()
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(completed=True).count()
        pending_tasks = Task.objects.filter(completed=False).count()
    else:
        tasks = Task.objects.filter(assigned_to=user)
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()
        pending_tasks = tasks.filter(completed=False).count()

    # Aplicar filtros si existen
    search = request.GET.get('search', '')
    filter_status = request.GET.get('filter', 'all')

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)

    # Solo administradores pueden ver la lista de usuarios para asignar
    users_list = User.objects.filter(groups__name='Usuario Limitado') if is_user_admin else []

    context = {
        'tasks': tasks,
        'search': search,
        'filter_status': filter_status,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'is_admin': is_user_admin,
        'users_list': users_list,
    }

    return render(request, 'tasks/task_list.html', context)


@login_required
def task_list_partial(request):
    """Vista parcial para actualizar solo la lista de tareas (HTMX)."""
    user = request.user
    is_user_admin = is_admin(user)
    
    if is_user_admin:
        tasks = Task.objects.all()
    else:
        tasks = Task.objects.filter(assigned_to=user)

    # Aplicar filtros
    search = request.GET.get('search', '')
    filter_status = request.GET.get('filter', 'all')

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)

    context = {
        'tasks': tasks,
        'is_admin': is_user_admin,
    }

    return render(request, 'tasks/partials/task_list_partial.html', context)


@login_required
@user_passes_test(is_admin, login_url='tasks:task_list')
@require_http_methods(["POST"])
def task_create(request):
    """Crea una nueva tarea (HTMX). Solo administradores."""
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
            'is_admin': True,
        }
        
        response = render(request, 'tasks/partials/task_item.html', context)
        response['HX-Trigger'] = 'taskCreated'
        return response
    
    except Exception:
        return HttpResponse(
            '<div class="text-red-500 text-sm mt-2">Error al crear la tarea</div>',
            status=500
        )


@login_required
@require_http_methods(["GET"])
def task_detail(request, pk):
    """Obtiene el detalle de una tarea para edición (HTMX)."""
    try:
        user = request.user
        is_user_admin = is_admin(user)
        
        if is_user_admin:
            task = get_object_or_404(Task, pk=pk)
        else:
            task = get_object_or_404(Task, pk=pk, assigned_to=user)
        
        users_list = User.objects.filter(groups__name='Usuario Limitado') if is_user_admin else []
        
        context = {
            'task': task,
            'is_admin': is_user_admin,
            'users_list': users_list,
        }
        return render(request, 'tasks/partials/task_edit_form.html', context)
    
    except Exception:
        return HttpResponse(
            '<div class="text-red-500 text-sm mt-2">Error al cargar la tarea</div>',
            status=500
        )


@login_required
@user_passes_test(is_admin, login_url='tasks:task_list')
@require_http_methods(["POST"])
def task_update(request, pk):
    """Actualiza una tarea existente (HTMX). Solo administradores."""
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
            'is_admin': True,
        }
        
        response = render(request, 'tasks/partials/task_item.html', context)
        response['HX-Trigger'] = 'taskUpdated'
        return response
    
    except Exception:
        return HttpResponse(
            '<div class="text-red-500 text-sm mt-2">Error al actualizar la tarea</div>',
            status=500
        )


@login_required
@require_http_methods(["POST"])
def task_toggle(request, pk):
    """Alterna el estado completado de una tarea (HTMX)."""
    try:
        user = request.user
        is_user_admin = is_admin(user)
        
        if is_user_admin:
            task = get_object_or_404(Task, pk=pk)
        else:
            task = get_object_or_404(Task, pk=pk, assigned_to=user)
        
        task.toggle_completed()

        context = {
            'task': task,
            'is_admin': is_user_admin,
        }
        
        response = render(request, 'tasks/partials/task_item.html', context)
        response['HX-Trigger'] = f'taskToggled:{{"completed": {str(task.completed).lower()}}}'
        return response
    
    except Exception:
        return HttpResponse(status=500)


@login_required
@user_passes_test(is_admin, login_url='tasks:task_list')
@require_http_methods(["DELETE"])
def task_delete(request, pk):
    """Elimina una tarea (HTMX). Solo administradores."""
    try:
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        
        response = HttpResponse('')
        response['HX-Trigger'] = 'taskDeleted'
        return response
    except Exception:
        return HttpResponse(status=500)


@login_required
def task_form_empty(request):
    """Retorna el formulario vacío para cancelar edición (HTMX)."""
    return render(request, 'tasks/partials/task_form.html')