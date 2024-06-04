def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try: 
            user = User.objects.get(username=username)
        except: 
            messages.error(request, "The user does not exist")
        
        user = authenticate(request, username=username, pasword=password)
        
        if user is not None:
            login(request, user)
            return redirect ('home')
        else:
            messages.error(request, 'Incorrect Password!')

    context = {}
    return render(request, 'base/login.html', context)