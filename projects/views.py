from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.constants import PROJECT_STATUS_CLOSED, PROJECT_STATUS_OPEN, PROJECTS_PER_PAGE
from core.services import paginate
from projects.forms import ProjectForm
from projects.models import Project


def project_list_view(request):
    projects = Project.objects.select_related('owner').prefetch_related(
        'participants').order_by('-created_at')
    page_obj = paginate(projects, PROJECTS_PER_PAGE, request.GET.get('page'))
    return render(request, 'projects/project_list.html', {
        'page_obj': page_obj,
        'query_prefix': '',
    })


def project_detail_view(request, project_id):
    project = get_object_or_404(
        Project.objects.select_related(
            'owner').prefetch_related('participants'),
        id=project_id,
    )
    return render(request, 'projects/project-details.html', {'project': project})


@login_required
def create_project_view(request):
    form = ProjectForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        project = form.save(commit=False)
        project.owner = request.user
        project.save()
        project.participants.add(request.user)
        return redirect(f'/projects/{project.id}/')
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': False,
    })


@login_required
def edit_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner:
        return redirect(f'/projects/{project_id}/')
    form = ProjectForm(request.POST or None, instance=project)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/projects/{project.id}/')
    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': True,
    })


@login_required
@require_POST
def complete_project_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.user != project.owner or project.status != PROJECT_STATUS_OPEN:
        return JsonResponse({'status': 'error'}, status=403)
    project.status = PROJECT_STATUS_CLOSED
    project.save()
    return JsonResponse({'status': 'ok', 'project_status': PROJECT_STATUS_CLOSED})


@login_required
@require_POST
def toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if user == project.owner or project.status == PROJECT_STATUS_CLOSED:
        return JsonResponse({'status': 'error'}, status=403)
    if user in project.participants.all():
        project.participants.remove(user)
        participating = False
    else:
        project.participants.add(user)
        participating = True
    return JsonResponse({'status': 'ok', 'participant': participating})


@login_required
@require_POST
def toggle_favorite_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    if project in user.favorites.all():
        user.favorites.remove(project)
        is_favorite = False
    else:
        user.favorites.add(project)
        is_favorite = True
    return JsonResponse({'status': 'ok', 'is_favorite': is_favorite})


@login_required
def favorites_view(request):
    projects = request.user.favorites.all().order_by('-created_at')
    return render(request, 'projects/favorite_projects.html', {'projects': projects})
