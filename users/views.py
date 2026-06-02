from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from core.constants import USERS_PER_PAGE
from core.services import paginate
from users.forms import ChangePasswordForm, EditProfileForm, LoginForm, RegisterForm
from users.models import User


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('/projects/list/')
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = form.cleaned_data['user']
        login(request, user)
        return redirect('/projects/list/')
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/projects/list/')


def user_detail_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/user-details.html', {'user': user})


@login_required
def edit_profile_view(request):
    form = EditProfileForm(request.POST or None,
                           request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect(f'/users/{request.user.id}/')
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password_view(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    if form.is_valid():
        form.save()
        # чтобы сессия не сбросилась после смены пароля
        login(request, request.user)
        return redirect(f'/users/{request.user.id}/')
    return render(request, 'users/change_password.html', {'form': form})


def participants_view(request):
    active_filter = request.GET.get('filter', '')
    users_qs = User.objects.filter(is_active=True).order_by('-id')

    if request.user.is_authenticated and active_filter:
        if active_filter == 'owners-of-favorite-projects':
            favorite_projects = request.user.favorites.all()
            users_qs = User.objects.filter(
                owned_projects__in=favorite_projects).distinct()
        elif active_filter == 'owners-of-participating-projects':
            participated_projects = request.user.participated_projects.all()
            users_qs = User.objects.filter(
                owned_projects__in=participated_projects).distinct()
        elif active_filter == 'interested-in-my-projects':
            my_projects = request.user.owned_projects.all()
            users_qs = User.objects.filter(
                favorites__in=my_projects).distinct()
        elif active_filter == 'participants-of-my-projects':
            my_projects = request.user.owned_projects.all()
            users_qs = User.objects.filter(
                participated_projects__in=my_projects).distinct()

    paginator = Paginator(users_qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginate(users_qs, USERS_PER_PAGE, request.GET.get('page'))

    query_prefix = f'filter={active_filter}&' if active_filter else ''

    return render(request, 'users/participants.html', {
        'page_obj': page_obj,
        'active_filter': active_filter,
        'query_prefix': query_prefix,
    })
