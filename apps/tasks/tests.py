from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task


class TaskModelTest(TestCase):
    """Tests para el modelo Task."""

    def setUp(self):
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description'
        )

    def test_task_creation(self):
        """Test de creación básica de tarea."""
        self.assertEqual(self.task.title, 'Test Task')
        self.assertEqual(self.task.description, 'Test Description')
        self.assertFalse(self.task.completed)
        self.assertIsNotNone(self.task.created_at)

    def test_task_str_method(self):
        """Test del método __str__."""
        self.assertEqual(str(self.task), '○ Test Task')
        self.task.completed = True
        self.task.save()
        self.assertEqual(str(self.task), '✓ Test Task')

    def test_toggle_completed(self):
        """Test del método toggle_completed."""
        initial_state = self.task.completed
        self.task.toggle_completed()
        self.assertEqual(self.task.completed, not initial_state)


class TaskAPITest(APITestCase):
    """Tests para la API de tareas."""

    def setUp(self):
        self.task = Task.objects.create(
            title='API Test Task',
            description='API Test Description'
        )
        self.list_url = reverse('tasks:task-list')
        self.detail_url = reverse('tasks:task-detail', kwargs={'pk': self.task.pk})

    def test_list_tasks(self):
        """Test de listado de tareas."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        """Test de creación de tarea."""
        data = {
            'title': 'New Task',
            'description': 'New Description'
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_create_task_validation(self):
        """Test de validación en creación de tarea."""
        data = {'title': 'AB'}  # Título muy corto
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_task(self):
        """Test de obtención de detalle de tarea."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Test Task')

    def test_update_task(self):
        """Test de actualización de tarea."""
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description'
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')

    def test_delete_task(self):
        """Test de eliminación de tarea."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.count(), 0)

    def test_toggle_task(self):
        """Test de toggle de estado completado."""
        toggle_url = reverse('tasks:task-toggle', kwargs={'pk': self.task.pk})
        initial_state = self.task.completed
        response = self.client.post(toggle_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.completed, not initial_state)

    def test_filter_by_completed(self):
        """Test de filtrado por estado completado."""
        Task.objects.create(title='Completed Task', description='Test', completed=True)
        response = self.client.get(self.list_url, {'completed': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_tasks(self):
        """Test de búsqueda de tareas."""
        Task.objects.create(title='Special Task', description='Test')
        response = self.client.get(self.list_url, {'search': 'Special'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)