from django.forms import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Project, Task
from .serializers import CreateProjectSerializer, AddProjectMembersSerializer, CreateTaskSerializer

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
        
        
class CreateTask(generics.CreateAPIView):
    queryset = Task.objects.filter(is_deleted=False)
    permission_classes = [IsAuthenticated]
    serializer_class = CreateTaskSerializer
