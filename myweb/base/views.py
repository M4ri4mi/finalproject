from django.shortcuts import render

def home(request):
    return render(request, 'base/home.html')

def login_view(request):
    return render(request, 'login.html')

    
