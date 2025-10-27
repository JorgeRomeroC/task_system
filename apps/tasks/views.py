from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Task


def task_list(request):
    tasks = Task.objects.all()

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
    }

    return render(request, 'tasks/task_list.html', context)


def task_list_partial(request):
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
    task = get_object_or_404(Task, pk=pk)
    context = {'task': task}
    return render(request, 'tasks/partials/task_edit_form.html', context)


@require_http_methods(["POST"])
def task_update(request, pk):
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
    task = get_object_or_404(Task, pk=pk)
    task.toggle_completed()

    context = {'task': task}
    return render(request, 'tasks/partials/task_item.html', context)


@require_http_methods(["DELETE"])
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()

    return HttpResponse('')


def task_form_empty(request):

    return render(request, 'tasks/partials/task_form.html')