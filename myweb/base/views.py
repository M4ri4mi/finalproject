from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

def home(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TaskForm(request.POST)
            print("Form data received:", request.POST)  # Debug: Print form data
            if form.is_valid():
                form.save()
                print("Form is valid and task is saved.")  # Debug: Print form validation success
                return redirect('home')
            else:
                print("Form is not valid:", form.errors)  # Debug: Print form errors
        else:
            form = TaskForm()

        tasks = Task.objects.all()
        print("Tasks retrieved:", tasks)  # Debug: Print tasks retrieved
        return render(request, 'base/home.html', {'tasks': tasks, 'form': form})
    else:
        return render(request, 'base/existing_page.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "The user does not exist")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Incorrect Password!')

    context = {}
    return render(request, 'base/login.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')

def profile(request):
    return render(request, 'base/profile.html')







    
