from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, export_views
from . import api_views

app_name = 'tasks'

# Router para la API REST
router = DefaultRouter()
router.register(r'tasks', api_views.TaskViewSet, basename='task')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),

    # Frontend endpoints (HTMX)
    path('', views.task_list, name='task_list'),
    path('partial/', views.task_list_partial, name='task_list_partial'),
    path('create/', views.task_create, name='task_create'),
    path('<int:pk>/', views.task_detail, name='task_detail'),
    path('<int:pk>/update/', views.task_update, name='task_update'),
    path('<int:pk>/toggle/', views.task_toggle, name='task_toggle'),
    path('<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('form-empty/', views.task_form_empty, name='task_form_empty'),

    # Export endpoints
    path('export/csv/', export_views.export_tasks_csv, name='export_csv'),
    path('export/excel/', export_views.export_tasks_excel, name='export_excel'),
    path('export/pdf/', export_views.export_tasks_pdf, name='export_pdf'),
]