from django import forms

from core.constants import PROJECT_STATUS_CHOICES
from core.mixins import GithubUrlValidationMixin
from projects.models import Project


class ProjectForm(GithubUrlValidationMixin, forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']
        widgets = {
            'status': forms.Select(choices=PROJECT_STATUS_CHOICES),
        }
