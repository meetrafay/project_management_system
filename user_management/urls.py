from django.urls import path
from .views import ListCreateProjectView, AddProjectMember, CreateTask

urlpatterns = [
    path('List_create_project/', ListCreateProjectView.as_view(), name='create_project'),
    path('add_project_members/', AddProjectMember.as_view(), name='add_project_member'),
    path('create_task/', CreateTask.as_view(), name='task')
]