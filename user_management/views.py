from django.forms import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Project, Task, TaskPermissions
from .serializers import CreateProjectSerializer, AddProjectMembersSerializer, CreateTaskSerializer, TaskSerializer

# Create your views here.
class ListCreateProjectView(generics.ListCreateAPIView):
    queryset = Project.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated]
    serializer_class = CreateProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AddProjectMember(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddProjectMembersSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        members = serializer.save()
        return Response({
            'status': True,
            'message': 'Project members added successfully',
            'data': {}
        }, status=status.HTTP_201_CREATED)
        
        
class DeleteProject(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        user = request.user
        project = Project.objects.filter(is_deleted=False, id=pk, created_by=user).first()
        
        if project:
            project.soft_delete()
            return Response({
                'status': True,
                'message': 'Project delete successfully',
                'data': {}
            }, status=status.HTTP_201_CREATED)
            
        else:
            return Response({
                'status': True,
                'message': 'No project found',
                'data': {}
            }, status=status.HTTP_404_NOT_FOUND)
        
        
class CreateTask(generics.CreateAPIView):
    queryset = Task.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTaskSerializer
    
    
    
class UpdateTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        task = Task.objects.filter(is_deleted=False, pk=pk, created_by=request.user).first()
        if task:
            
            serializer = TaskSerializer(task, data=request.data, partial=True)

            if serializer.is_valid():
                # Check if the user has the 'can_update' permission for this task
                task_permissions = TaskPermissions.objects.filter(project=task.project, user=request.user, permission='can_update')
                if task_permissions.exists():
                    serializer.save()
                    return Response({'message': 'Task updated successfully',
                                     'data':serializer.data})
                else:
                    return Response({'error': 'You do not have permission to update this task'}, status=status.HTTP_200_OK)
            return Response(serializer.errors)
    
        else:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        task = Task.objects.filter(is_deleted=False, pk=pk, created_by=request.user).first()
        if task:

            task_permissions = TaskPermissions.objects.filter(project=task.project, user=request.user, permission='can_delete')
            if task_permissions.exists():
                task.soft_delete() 
                return Response({'message': 'Task deleted successfully'})
            else:
                return Response({'error': 'You do not have permission to delete this task'}, status=status.HTTP_200_OK)
            
        else:
            return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        
        
class GetTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        project = Project.objects.filter(id=pk).first()
        
        if project:
            task_permissions = TaskPermissions.objects.filter(project=project, user=request.user, permission='can_view')
            
            if task_permissions.exists():
                tasks = Task.objects.filter(project=project, is_deleted=False)
                serializer = TaskSerializer(tasks, many=True)
                return Response({'message': 'Tasks fetched successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
            
            else:
                return Response({'error': 'You do not have permission to view tasks'}, status=status.HTTP_403_FORBIDDEN)   
        
        else:
            return Response({'error': 'No project found'}, status=status.HTTP_404_NOT_FOUND)
            