from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm

# Create your views here.
def register_view(request):
    if request.method =="POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"your account has been created successfully!")
            return redirect("home")
    else:
        form = RegistrationForm()

    return render(request,"accounts/register.html",{"form":form},)    

def login_views(request):
    if request.method == "POST":
        form =AuthenticationForm(request,data=request.POST,)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    else:
        form = AuthenticationForm(request)
    return render(request,"accounts/login.html",{"form":form},)

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("home")
def home(request):
    return render(request, "home.html")