from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project')


class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('INPROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='TODO')
    due_date = models.DateField()
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()


class TaskPermissions(models.Model):
    PERMISSION_CHOICES = [
        ('can_create', 'Can Create'),
        ('can_update', 'Can Update'),
        ('can_delete', 'Can Delete'),
        ('can_view', 'Can View'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES)