from django.db import models

from users.models import User


class Project(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='owned_projects')
    created_at = models.DateField(auto_now_add=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=6, choices=STATUS_CHOICES, default='open')
    participants = models.ManyToManyField(
        User, blank=True, related_name='participated_projects')

    def __str__(self):
        return self.name
