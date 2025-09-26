from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import userdetails as register
from .models import studentdetails

# Create your views here.

def index_view(request):
    return render(request, 'index.html')

def studysessions(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access the dashboard.")
        return redirect('login')

    username = request.session.get('username')

    # Assuming studentname corresponds to the logged-in user
    user_student_records = studentdetails.objects.filter(studentname=username)

    # Pass user student records as both study_sessions and courses (since you have only studentdetails model)
    return render(request, 'studysession.html', {
        'username': username,
        'study_sessions': user_student_records,  # can map course_name, date, duration accordingly in template
        'courses': user_student_records,
    })


def studentcourses(request):
    return render(request, 'studentcourse.html')

def newstudent_view(request):
    return render(request, 'newstudent.html')


def userdashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access the dashboard.")
        return redirect('login')
    
    username = request.session.get('username')

    # Filter student records for only this user
    user_students = studentdetails.objects.filter(studentname=username)
    
    return render(request, 'userdashboard.html', {'username': username, 'students': user_students})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
 
        try:
            user = register.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
 
            messages.success(request, f"Welcome {user.username} !")
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


def admindashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access the dashboard.")
        return redirect('adminlogin')
    
    username = request.session.get('username')
    students = studentdetails.objects.all()
    return render(request, 'admindashboard.html', {'username': username, 'students': students})

def adminlogin_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
 
        try:
            user = register.objects.get(username=username, password=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
 
            messages.success(request, f"Wellcome {user.username} !")
            return redirect('admindashboard')
        except register.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect('adminlogin')
 
    return render(request, 'adminlogin.html')


def add_student_view(request):
    if request.method == "POST":
        studentname = request.POST['studentname']
        coursename = request.POST['coursename']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        hoursspent = request.POST['hoursspent']
        completion = request.POST['completion']
        status = request.POST['status']

        # Save to DB
        student = studentdetails(
            studentname=studentname,
            coursename=coursename,
            startdate=startdate,
            enddate=enddate,
            hoursspent=hoursspent,
            completion=completion,
            status=status
        )
        student.save()

        messages.success(request, "Student details added successfully!")
        return redirect('admindashboard')  # redirect back to form or dashboard

    return render(request, 'newstudent.html')  # replace with your form template