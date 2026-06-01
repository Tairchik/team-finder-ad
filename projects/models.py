from django.db import models

from core.constants import (
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_STATUS_CHOICES,
    PROJECT_STATUS_MAX_LENGTH,
    PROJECT_STATUS_OPEN,
)
from users.models import User


class Project(models.Model):
    name = models.CharField(max_length=PROJECT_NAME_MAX_LENGTH)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateField(auto_now_add=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=PROJECT_STATUS_MAX_LENGTH,
        choices=PROJECT_STATUS_CHOICES,
        default=PROJECT_STATUS_OPEN,
    )
    participants = models.ManyToManyField(
        User, blank=True, related_name='participated_projects')

    def __str__(self):
        return self.name
