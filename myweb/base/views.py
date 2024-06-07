from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task, Plan, Profile
from .forms import TaskForm, PlanForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
import json


@login_required
def home(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()
        plan_form = PlanForm()

    tasks = Task.objects.filter(user=request.user)
    plans = Plan.objects.filter(user=request.user)
    return render(request, 'base/home.html', {'tasks': tasks, 'form': form, 'plans': plans, 'plan_form': plan_form})

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
            return redirect('profile')  # Redirect to the same profile page
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'base/profile.html', {
        'form': form,
        'username': request.user.username,
    })

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'base/task_detail_content.html', {'task': task})
    return render(request, 'base/task_detail.html', {'task': task})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Task updated successfully'})
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'base/task_form.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Task deleted successfully'})
        return redirect('home')
    return render(request, 'base/task_confirm_delete.html', {'task': task})

# Plan CRUD
@login_required
def create_plan(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('home')
    else:
        form = PlanForm()
    return render(request, 'base/plan_form.html', {'form': form})

@login_required
def update_plan(request, pk):
    plan = get_object_or_404(Plan, id=pk)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Plan updated successfully'})
            return redirect('home')
    else:
        form = PlanForm(instance=plan)
    return render(request, 'base/plan_form.html', {'form': form})

@login_required
def delete_plan(request, pk):
    plan = get_object_or_404(Plan, id=pk)
    if request.method == "POST":
        plan.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Plan deleted successfully'})
        return redirect('home')
    return render(request, 'base/plan_confirm_delete.html', {'plan': plan})

@login_required
def plan_list(request):
    plans = Plan.objects.filter(user=request.user)
    return render(request, 'base/plan_list.html', {'plans': plans})











    
