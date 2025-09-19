from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import userdetails as register

# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def userdashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access the dashboard.")
        return redirect('login')
    
    username = request.session.get('username')
    return render(request, 'userdashboard.html', {'username': username})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
 
        try:
            user = register.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
 
            messages.success(request, f"Welcome {user.username}!")
            return redirect('userdashboard')
        except register.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect('login')
 
    return render(request, 'login.html')


def registration_view(request):
    if request.method == "POST":
        fullname = request.POST['fullname']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
 
        if password != confirmpassword:
            messages.error(request, "Passwords do not match")
            return render(request, 'register.html')
       
        if register.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please login.")
            return redirect('login')
       
        if register.objects.filter(username=username).exists():
            messages.error(request, "Username already taken. Please choose another.")
            return render(request, 'register.html')
 
        reg = register(
            fullname=fullname,
            email=email,
            username=username,
            password=password
        )
        reg.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
 
    return render(request, 'register.html')