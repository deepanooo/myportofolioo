import uuid
from django.db import models
from django.utils import timezone


class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, default="volunteer")
    started_at = models.DateField(default=timezone.now)
    ended_at = models.DateField(null=True, blank=True)

    @property
    def is_ongoing(self):
        return self.ended_at is None

    def __str__(self):
        return self.title


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    repository_url = models.URLField(blank=True, default="")
    project_image_url = models.URLField(blank=True, default="", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
