from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import Profile

def home_auth(request):
    return render(request, "registration/home_auth.html")
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("register:login")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("main:home")
        else:
            messages.error(request, "Невірний логін або пароль")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})




def logout_view(request):
    logout(request)
    return redirect("register:login")