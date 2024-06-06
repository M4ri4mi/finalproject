# base/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task, Plan, Profile
from .forms import TaskForm, PlanForm, ProfileForm
from django.contrib.auth.forms import UserCreationForm

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user  # Set the user to the currently logged-in user
                task.save()
                messages.success(request, 'Task added successfully!')
                return redirect('home')
        else:
            form = TaskForm()
            plan_form = PlanForm()

        tasks = Task.objects.filter(user=request.user)
        plans = Plan.objects.filter(user=request.user)
        return render(request, 'base/home.html', {'tasks': tasks, 'form': form, 'plans': plans, 'plan_form': plan_form})
    else:
        return render(request, 'base/existing_page.html')

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

def profile(request):
    return render(request, 'base/profile.html')

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'base/task_detail.html', {'task': task})

@login_required
def task_update(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'base/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('home')
    return render(request, 'base/task_confirm_delete.html', {'task': task})

# Plan CRUD
@login_required(login_url='login')
def create_plan(request):
    form = PlanForm()
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user  # Set the user to the currently logged-in user
            plan.save()
            messages.success(request, 'Plan created successfully!')
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/plan_form.html', context)

@login_required(login_url='login')
def update_plan(request, pk):
    plan = get_object_or_404(Plan, id=pk)
    form = PlanForm(instance=plan)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Plan updated successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Error updating plan.')
    context = {'form': form}
    return render(request, 'base/plan_form.html', context)

@login_required(login_url='login')
def delete_plan(request, pk):
    plan = get_object_or_404(Plan, id=pk)
    if request.method == "POST":
        plan.delete()
        messages.success(request, 'Plan deleted successfully!')
        return redirect('home')
    return render(request, "base/delete.html", {'obj': plan})

@login_required(login_url='login')
def plan_list(request):
    plans = Plan.objects.filter(user=request.user)
    return render(request, 'base/plan_list.html', {'plans': plans})


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










    
