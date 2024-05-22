from django.urls import path
from .views import ListCreateProjectView, AddProjectMember, CreateTask, UpdateTaskView, DeleteTaskView, GetTasksView

urlpatterns = [
    path('List_create_project/', ListCreateProjectView.as_view(), name='create_project'),
    path('add_project_members/', AddProjectMember.as_view(), name='add_project_member'),
    path('create_task/', CreateTask.as_view(), name='task'),
    path('update_task/<int:pk>/', UpdateTaskView.as_view(), name='update_task'),
    path('delete_task/<int:pk>/', DeleteTaskView.as_view(), name='delete_task'),
    path('list_task/<int:pk>/', GetTasksView.as_view(), name='list_task')
]