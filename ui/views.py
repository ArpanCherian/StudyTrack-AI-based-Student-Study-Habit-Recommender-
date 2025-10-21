from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import userdetails as register
from .models import admindetails as adminregister
from .models import studentdetails
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import studentdetails, userdetails
from .models import Notification

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
        # can map course_name, date, duration accordingly in template
        'study_sessions': user_student_records,
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
            messages.error(
                request, "Username already taken. Please choose another.")
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
        username = request.POST['adminusername']
        password = request.POST['adminpassword']

        try:
            user = adminregister.objects.get(
                adminusername=username, adminpassword=password)
            request.session['user_id'] = user.id
            request.session['username'] = user.adminusername

            messages.success(request, f"Wellcome {user.adminusername} !")
            return redirect('admindashboard')
        except adminregister.DoesNotExist:
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

    # replace with your form template
    return render(request, 'newstudent.html')


def ongoing_course(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access the dashboard.")
        return redirect('adminlogin')
    # Get all students with 'Ongoing' or 'Not Started' status
    students = studentdetails.objects.filter(
        status__in=['Ongoing', 'Not Started']
    )
    return render(request, 'ongoing_course.html', {'students': students})


def send_course_reminder(request):
    if request.method == "POST":
        students = studentdetails.objects.filter(
            status__in=['Ongoing', 'Not Started'])
        email_count = 0
        for student in students:
            try:
                user = userdetails.objects.get(username=student.studentname)
                send_mail(
                    subject="Reminder: Complete your course",
                    message=(
                        f"Dear {user.fullname},\n\n"
                        f"Your course '{student.coursename}' is not complete ({student.completion}%). "
                        "Please log in and complete your course as soon as possible."
                    ),
                    from_email="arpanjacobcherian@gmail.com",  # Replace appropriately
                    recipient_list=[user.email],
                    )
                    # Create a notification
                Notification.objects.create(
                        student=user,
                        message=f"Reminder: Please complete your course '{student.coursename}'. Completion: {student.completion}%"
                    )
                email_count += 1
            except userdetails.DoesNotExist:
                continue
        messages.success(request, f"Sent reminders to {email_count} students.")
        return redirect('ongoing_course')  # Change as needed
    # For GET requests, redirect to ongoing_course
    return redirect('ongoing_course')


def usernotification(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access notifications.")
        return redirect('login')
    user = userdetails.objects.get(pk=request.session['user_id'])
    notifications = Notification.objects.filter(student=user).order_by('-created_at')
    return render(request, 'usernotification.html', {
        'notifications': notifications,
        'username': user.username
    })


