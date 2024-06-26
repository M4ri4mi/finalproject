# base/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note, Task, Profile, Project, Tag
from .forms import NoteForm, TaskForm, ProfileForm, ProjectForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.http import JsonResponse
import random
from django.db.models import Q
from django.utils import timezone



def home(request):
    if request.user.is_authenticated:
        today_date = date.today()
        tasks = Task.objects.filter(user=request.user, date_added=today_date)
        projects = Project.objects.filter(user=request.user)
        notes = Note.objects.filter(user=request.user)
        tags = Tag.objects.all()
        note_form = NoteForm()
        task_form = TaskForm()
        project_form = ProjectForm()

        completed_tasks = tasks.filter(is_done=True).count()
        total_tasks = tasks.count()
        task_ratio = f"{completed_tasks}/{total_tasks}" if total_tasks > 0 else "0/0"

        completed_projects = projects.filter(is_done=True).count()
        total_projects = projects.count()
        project_ratio = f"{completed_projects}/{total_projects}" if total_projects > 0 else "0/0"

        if request.method == 'POST':
            if 'task_form' in request.POST:
                task_form = TaskForm(request.POST)
                if task_form.is_valid():
                    task = task_form.save(commit=False)
                    task.user = request.user
                    task.save()
                    task_form.save_m2m()
                    messages.success(request, 'Task created successfully')
                    return redirect('home')
            elif 'note_form' in request.POST:
                note_form = NoteForm(request.POST)
                if note_form.is_valid():
                    note = note_form.save(commit=False)
                    note.user = request.user
                    note.save()
                    note_form.save_m2m()
                    messages.success(request, 'Note created successfully')
                    return redirect('home')
            elif 'project_form' in request.POST:
                project_form = ProjectForm(request.POST)
                if project_form.is_valid():
                    project = project_form.save(commit=False)
                    project.user = request.user
                    project.save()
                    project_form.save_m2m()
                    messages.success(request, 'Project created successfully')
                    return redirect('home')

        today_date_str = today_date.strftime("%B %d, %Y")

        return render(request, 'base/home.html', {
            'notes': notes,
            'tasks': tasks,
            'projects': projects,
            'tags': tags,
            'note_form': note_form,
            'task_form': task_form,
            'project_form': project_form,
            'today_date': today_date_str,
            'task_ratio': task_ratio,
            'project_ratio': project_ratio,
        })
    else:
        return render(request, 'base/existing_page.html')


@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully')
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'base/task_form.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully')
        return redirect('home')
    return render(request, 'base/task_confirm_delete.html', {'task': task})

@login_required
def mark_task_done(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.is_done = True
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@login_required
def toggle_task_done(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        task.is_done = not task.is_done
        task.save()
        return JsonResponse({'success': True, 'is_done': task.is_done})
    return JsonResponse({'success': False})

@login_required
def update_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully')
            return redirect('home')
    else:
        form = NoteForm(instance=note)
    return render(request, 'base/note_form.html', {'form': form})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Note deleted successfully')
        return redirect('home')
    return render(request, 'base/note_confirm_delete.html', {'note': note})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password.')
    return render(request, 'base/login.html', {'page': 'login'})

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration.")
    return render(request, 'base/login.html', {'page': 'register', 'form': form})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'base/profile.html', {
        'form': form,
        'username': request.user.username,
    })

@login_required
def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully')
            return redirect('home')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'base/project_form.html', {'form': form})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully')
        return redirect('home')
    return render(request, 'base/project_confirm_delete.html', {'project': project})

@login_required
def toggle_project_done(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.is_done = not project.is_done
        project.save()
        return JsonResponse({'success': True, 'is_done': project.is_done})
    return JsonResponse({'success': False})

def search_results(request):
    query = request.GET.get('q')
    if query:
        notes = Note.objects.filter(Q(content__icontains=query), user=request.user)
        tasks = Task.objects.filter(Q(content__icontains=query), user=request.user)
        projects = Project.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query), user=request.user
        )
    else:
        notes = tasks = projects = []

    return render(request, 'base/search_results.html', {
        'query': query,
        'notes': notes,
        'tasks': tasks,
        'projects': projects,
    })

@login_required
def overdue_projects(request):
    current_date = timezone.now().date()
    overdue_projects = Project.objects.filter(user=request.user, due_date__lt=current_date, is_done=False)
    return render(request, 'base/overdue_projects.html', {'overdue_projects': overdue_projects})

@login_required
def upcoming_projects(request):
    current_date = timezone.now().date()
    upcoming_projects = Project.objects.filter(user=request.user, due_date__gte=current_date, is_done=False)
    return render(request, 'base/upcoming_projects.html', {'upcoming_projects': upcoming_projects})

@login_required
def recent_tasks(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user).order_by('-date_added')
        tasks_by_date = {}
        for task in tasks:
            date_str = task.date_added.strftime("%B %d, %Y")
            if date_str not in tasks_by_date:
                tasks_by_date[date_str] = []
            tasks_by_date[date_str].append(task)

        return render(request, 'base/recent_tasks.html', {
            'tasks_by_date': tasks_by_date,
        })

@login_required
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'base/tag_list.html', {'tags': tags})

@login_required
def filter_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    tasks = Task.objects.filter(user=request.user, tags=tag)
    notes = Note.objects.filter(user=request.user, tags=tag)
    projects = Project.objects.filter(user=request.user, tags=tag)
    return render(request, 'base/filter_by_tag.html', {
        'tag': tag,
        'tasks': tasks,
        'notes': notes,
        'projects': projects
    })