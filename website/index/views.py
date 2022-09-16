from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import 

# Create your views here.
def index(request):
    return render(request, "index/index.html")

def login_view(request):
    # From index page, login link
    if request.method == "GET":
        return render(request, "index/login.html")

    # From login page, form submittion to create user
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'index/index.html')

        else:
            return render(request, 'index/login.html', {
                'error': 'User does not exist'
            })

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'index/index.html')