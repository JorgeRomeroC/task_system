from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer, TaskListSerializer, TaskToggleSerializer


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_serializer_class(self):

        if self.action == 'list':
            return TaskListSerializer
        elif self.action == 'toggle':
            return TaskToggleSerializer
        return TaskSerializer

    def get_queryset(self):

        queryset = Task.objects.all()

        # Filtro de búsqueda
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Filtro por estado completado
        completed = self.request.query_params.get('completed', None)
        if completed is not None:
            if completed.lower() == 'true':
                queryset = queryset.filter(completed=True)
            elif completed.lower() == 'false':
                queryset = queryset.filter(completed=False)

        return queryset

    @action(detail=True, methods=['post', 'patch'])
    def toggle(self, request, pk=None):

        task = self.get_object()
        task.toggle_completed()

        serializer = self.get_serializer(task)
        return Response(
            {
                'success': True,
                'message': f'Tarea marcada como {"completada" if task.completed else "pendiente"}',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            {
                'success': True,
                'message': 'Tarea creada exitosamente',
                'data': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            {
                'success': True,
                'message': 'Tarea actualizada exitosamente',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):

        instance = self.get_object()
        self.perform_destroy(instance)

        return Response(
            {
                'success': True,
                'message': 'Tarea eliminada exitosamente'
            },
            status=status.HTTP_200_OK
        )