from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = TaskForm()

        tasks = Task.objects.all()
        return render(request, 'base/home.html', {'tasks': tasks, 'form': form})
    else:
        return render(request, 'base/existing_page.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def login_view(request):
    page = "login"
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "The user does not exist")
            return render(request, 'base/login.html', {'page': page})

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Password!')

    context = {"page": page}
    return render(request, 'base/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def register_page(request):
    page = "register"
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
            messages.error(request, "An Error Occurred")

    return render(request, 'base/login.html', {"form": form, "page": page})



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
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render(request, 'base/task_form.html', {'form': form, 'task': task})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('home')
    return render(request, 'base/task_confirm_delete.html', {'task': task})



   














    
