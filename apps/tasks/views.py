from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Task

@login_required
def task_list(request):
    """Vista principal que renderiza la lista de tareas."""
    tasks = Task.objects.all()

    # Calcular estadísticas ANTES de aplicar filtros
    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    pending_tasks = Task.objects.filter(completed=False).count()

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

    context = {
        'tasks': tasks,
        'search': search,
        'filter_status': filter_status,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
    }

    return render(request, 'tasks/task_list.html', context)


def task_list_partial(request):
    """Vista parcial para actualizar solo la lista de tareas (HTMX)."""
    tasks = Task.objects.all()

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
    }

    return render(request, 'tasks/partials/task_list_partial.html', context)


@require_http_methods(["POST"])
def task_create(request):
    """Crea una nueva tarea (HTMX)."""
    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()

    if not title or len(title) < 3:
        return HttpResponse(
            '<div class="text-red-500 text-sm mt-2">El título debe tener al menos 3 caracteres</div>',
            status=400
        )

    task = Task.objects.create(
        title=title,
        description=description
    )

    context = {'task': task}
    return render(request, 'tasks/partials/task_item.html', context)


@require_http_methods(["GET"])
def task_detail(request, pk):
    """Obtiene el detalle de una tarea para edición (HTMX)."""
    task = get_object_or_404(Task, pk=pk)
    context = {'task': task}
    return render(request, 'tasks/partials/task_edit_form.html', context)


@require_http_methods(["POST"])
def task_update(request, pk):
    """Actualiza una tarea existente (HTMX)."""
    task = get_object_or_404(Task, pk=pk)

    title = request.POST.get('title', '').strip()
    description = request.POST.get('description', '').strip()

    if not title or len(title) < 3:
        return HttpResponse(
            '<div class="text-red-500 text-sm mt-2">El título debe tener al menos 3 caracteres</div>',
            status=400
        )

    task.title = title
    task.description = description
    task.save()

    context = {'task': task}
    return render(request, 'tasks/partials/task_item.html', context)


@require_http_methods(["POST"])
def task_toggle(request, pk):
    """Alterna el estado completado de una tarea (HTMX)."""
    task = get_object_or_404(Task, pk=pk)
    task.toggle_completed()

    context = {'task': task}
    return render(request, 'tasks/partials/task_item.html', context)


@require_http_methods(["DELETE"])
def task_delete(request, pk):
    """Elimina una tarea (HTMX)."""
    task = get_object_or_404(Task, pk=pk)
    task.delete()

    # Retornar respuesta vacía para que HTMX elimine el elemento
    return HttpResponse('')


def task_form_empty(request):
    """Retorna el formulario vacío para cancelar edición (HTMX)."""
    return render(request, 'tasks/partials/task_form.html')