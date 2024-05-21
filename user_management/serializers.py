from rest_framework import serializers
from .models import Project, ProjectMember
from django.contrib.auth.models import User


class CreateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'is_deleted', 'deleted_at']
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True}
        }

class AddProjectMembersSerializer(serializers.Serializer):
    project_id = serializers.IntegerField()
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

    def validate_project_id(self, value):
        try:
            project = Project.objects.get(id=value, is_deleted=False)
        except Project.DoesNotExist:
            raise serializers.ValidationError("Project does not exist.")
        return value

    def validate_user_ids(self, value):
        if not value:
            raise serializers.ValidationError("User IDs list cannot be empty.")
        users = User.objects.filter(id__in=value)
        if users.count() != len(value):
            raise serializers.ValidationError("One or more users do not exist.")
        return value

    def create(self, validated_data):
        print("=====",validated_data)
        project = Project.objects.get(id=validated_data['project_id'])
        user_ids = validated_data['user_ids']
        project_members = []
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            if not ProjectMember.objects.filter(project=project, user=user).exists():
                project_members.append(ProjectMember(project=project, user=user))
            else:
                raise serializers.ValidationError(f"{user.id} User already added to project.")

        # Use bulk_create with ignore_conflicts=True to avoid IntegrityError for duplicates
        ProjectMember.objects.bulk_create(project_members, ignore_conflicts=True)

        return project_members