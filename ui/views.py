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
from django.utils import timezone
from .models import Quiz, QuizAttempt
from .models import Course
from .models import userdetails



# At the top of views.py
COURSES = [
    {
        'name': 'Cybersecurity',
        'description': 'Computer security (also cybersecurity, digital security, or information technology (IT) security) is a subdiscipline within the field of information security.',
        'duration': '6 months',
        'image': 'cybersecurity.webp'
    },
    {
        'name': 'Data Analytics',
        'description': 'Fundamentals of classical mechanics and motion to build strong basics.',
        'duration': '4 months',
        'image': 'data analytics.webp'
    },
    {
        'name': 'Computer Science - Python',
        'description': 'Learn Python programming fundamentals and advance to web development.',
        'duration': '3 months',
        'image': 'python.webp'
    },
    {
        'name': 'Web Development',
        'description': 'Study organic compounds, reactions, and mechanisms in this comprehensive course.',
        'duration': '5 months',
        'image': 'Web Development.webp'
    },
    {
        'name': 'Blockchain',
        'description': 'Explore classic and contemporary literature and improve your critical thinking.',
        'duration': '4 months',
        'image': 'Blockchain.webp'
    },
    {
        'name': 'Cloud Computing',
        'description': 'Understand the fundamentals of genetics and heredity in this detailed course.',
        'duration': '4 months',
        'image': 'cloud Computing.webp'
    }
]

# Create your views here.


def index_view(request):
    return render(request, 'index.html')


def studysessions(request):
    if 'user_id' not in request.session:
        messages.error(request, "Please login to access the dashboard.")
        return redirect('login')

    username = request.session.get('username')
    user = userdetails.objects.get(username=username)

    # All courses the student is enrolled in
    enrolled_courses = studentdetails.objects.filter(studentname=user.username).values_list('coursename', flat=True)
    
    # Collect list of incompleted quizzes per course
    incomplete_quizzes = []
    for coursename in enrolled_courses:
        attempt = QuizAttempt.objects.filter(student=user, coursename=coursename, completed=True).first()
        quiz_exists = Quiz.objects.filter(course__name=coursename).exists()
        if not attempt and quiz_exists:
            incomplete_quizzes.append(coursename)

    user_student_records = studentdetails.objects.filter(studentname=username)

    return render(request, 'studysession.html', {
        'username': username,
        'study_sessions': user_student_records,
        'courses': user_student_records,
        'incomplete_quizzes': incomplete_quizzes
    })






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
        return redirect('admindashboard')
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


from django.core.mail import send_mail
from django.contrib import messages

def send_course_reminder(request):
    if request.method == "POST":
        students = studentdetails.objects.filter(
            status__in=['Ongoing', 'Not Started']
        )
        email_count = 0
        failed_list = []
        for student in students:
            try:
                user = userdetails.objects.get(username=student.studentname)
                # Compose message
                msg = (
                    f"Dear {user.fullname},\n\n"
                    f"Your course '{student.coursename}' is not complete ({student.completion}%). "
                    "Please log in and complete your course as soon as possible."
                )
                send_mail(
                    subject="Reminder: Complete your course",
                    message=msg,
                    from_email="arpanjacobcherian@gmail.com",  # use the one in settings
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                Notification.objects.create(
                    student=user,
                    message=f"Reminder: Please complete your course '{student.coursename}'. Completion: {student.completion}%"
                )
                email_count += 1
            except Exception as e:
                failed_list.append(f"{student.studentname}: {str(e)}")
                continue
        summary_msg = f"Sent reminders to {email_count} students."
        if failed_list:
            summary_msg += " Errors: " + "; ".join(failed_list)
        messages.success(request, summary_msg)
        return redirect('ongoing_course')
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Course, studentdetails, userdetails, Quiz
from django.utils import timezone

def studentcourses(request):
    if 'username' not in request.session:
        return redirect('login')

    username = request.session['username']
    user = userdetails.objects.get(username=username)

    # Get courses enrolled
    enrolled_names = set(studentdetails.objects.filter(studentname=user.username).values_list('coursename', flat=True))

    # Mark enrollment state for every course
    courses = []
    for course in COURSES:
        course_copy = course.copy()
        course_copy['enrolled'] = course['name'] in enrolled_names
        courses.append(course_copy)

    # Calculate completion rate for each course
    course_stats = []
    for course in COURSES:
        total_enrolled = studentdetails.objects.filter(coursename=course['name']).count()
        completed = studentdetails.objects.filter(coursename=course['name'], status='Completed').count()
        completion_rate = round((completed / total_enrolled) * 100, 2) if total_enrolled > 0 else 0
        
        course_stats.append({
            'name': course['name'],
            'image': course['image'],
            'description': course['description'],
            'completion_rate': completion_rate,
            'total_enrolled': total_enrolled,
            'enrolled': course['name'] in enrolled_names
        })

    # Get top course (not already enrolled)
    available_courses = [c for c in course_stats if not c['enrolled']]
    top_course = max(available_courses, key=lambda x: x['completion_rate']) if available_courses else None

    return render(request, 'studentcourse.html', {
        'courses': courses,
        'user': user,
        'top_course': top_course
    })



def enroll_course(request, coursename):
    if 'username' not in request.session:
        messages.error(request, "You must log in to enroll in a course.")
        return redirect('login')

    username = request.session['username']
    user = get_object_or_404(userdetails, username=username)

    # Prevent duplicate enrollments
    if studentdetails.objects.filter(studentname=user.username, coursename=coursename).exists():
        messages.info(request, f"You are already enrolled in {coursename}.")
        return redirect('allcourse', coursename=coursename)

    # Create studentdetails entry to register enrollment
    studentdetails.objects.create(
        studentname=user.username,
        coursename=coursename,
        startdate=timezone.now().date(),
        enddate=timezone.now().date().replace(
            month=timezone.now().month + 3) if timezone.now().month < 10 else timezone.now().date().replace(
            year=timezone.now().year + 1, month=(timezone.now().month + 3) % 12),
        hoursspent=0,
        completion=0,
        status='Ongoing',
    )
    messages.success(request, f"You have successfully enrolled in {coursename}!")
    return redirect('allcourse', coursename=coursename)


def allcourse(request, coursename):
    if 'username' not in request.session:
        messages.error(request, "Please login to view the course details.")
        return redirect('login')

    username = request.session['username']
    user = userdetails.objects.get(username=username)

    enrolled = studentdetails.objects.filter(studentname=user.username, coursename=coursename).first()
    all_enrollments = studentdetails.objects.filter(coursename=coursename)
    total_students = all_enrollments.count()
    completed = all_enrollments.filter(status='Completed').count()
    completion_rate = round((completed / total_students) * 100, 2) if total_students > 0 else 0

    course_obj = Course.objects.filter(name=coursename).first()
    if course_obj is None:
        messages.error(request, "Course not found.")
        return redirect('studentcourses')

    videos = course_obj.videos.all()
    course_info = next((c for c in COURSES if c['name'] == coursename), None)

    # Quiz Attempt Logic
    quizattempt = None
    if enrolled:
        quizattempt = QuizAttempt.objects.filter(student=user, coursename=coursename).first()

    context = {
        'coursename': coursename,
        'description': course_obj.description,
        'duration': course_obj.duration,
        'courseimage': course_info['image'] if course_info else "",
        'total_students': total_students,
        'completed': completed,
        'completion_rate': completion_rate,
        'enrolled': enrolled,
        'videos': videos,
        'quizattempt': quizattempt,
    }
    return render(request, 'allcourse.html', context)





from .models import Quiz, QuizAttempt, userdetails, studentdetails

def take_quiz(request, coursename):
    if 'username' not in request.session:
        return redirect('login')
    username = request.session['username']
    user = userdetails.objects.get(username=username)

    # Prevent retake if already completed
    attempt = QuizAttempt.objects.filter(student=user, coursename=coursename, completed=True).first()
    if attempt:
        messages.info(request, "Quiz already completed for this course.")
        return render(request, 'quiz_completed.html', {'score': attempt.score})

    quizzes = Quiz.objects.filter(course__name=coursename)
    if request.method == "POST":
        correct = 0
        total = quizzes.count()
        for quiz in quizzes:
            selected = request.POST.get(f"quiz_{quiz.id}")
            if selected == quiz.correct_answer:
                correct += 1
        score = int((correct / total) * 100) if total else 0

        # Save quiz attempt
        QuizAttempt.objects.update_or_create(
            student=user, coursename=coursename,
            defaults={'score': score, 'completed': True}
        )

        # Mark studentdetails as complete (optional)
        student = studentdetails.objects.filter(studentname=user.fullname, coursename=coursename).first()
        if student and student.status != 'Completed':
            student.status = 'Completed'
            student.completion = 100
            student.save()

        return render(request, 'quiz_completed.html', {'score': score})

    context = {
        'coursename': coursename,
        'quizzes': quizzes,
    }
    return render(request, 'quiz.html', context)



from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import VideoProgress, CourseVideo, studentdetails, userdetails

@require_POST
def mark_video_watched(request):
    if 'username' not in request.session:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    video_id = request.POST.get('video_id')
    coursename = request.POST.get('coursename')
    
    username = request.session['username']
    user = userdetails.objects.get(username=username)
    video = CourseVideo.objects.get(id=video_id)
    
    # Mark video as watched
    VideoProgress.objects.update_or_create(
        student=user,
        video=video,
        defaults={'watched': True}
    )
    
    # Calculate progress
    total_videos = CourseVideo.objects.filter(course__name=coursename).count()
    watched_videos = VideoProgress.objects.filter(
        student=user,
        video__course__name=coursename,
        watched=True
    ).count()
    
    progress = int((watched_videos / total_videos) * 100) if total_videos > 0 else 0
    
    # Update studentdetails completion and status
    student_record = studentdetails.objects.filter(
        studentname=user.username,
        coursename=coursename
    ).first()
    
    if student_record:
        student_record.completion = progress
        
        # Automatically mark as Completed when progress reaches 100%
        if progress >= 100:
            student_record.status = 'Completed'
        elif progress > 0:
            student_record.status = 'Ongoing'
        
        student_record.save()
    
    return JsonResponse({
        'success': True,
        'progress': progress,
        'watched_videos': watched_videos,
        'total_videos': total_videos,
        'status': student_record.status if student_record else 'Unknown'
    })



from .recommender import recommend_best_course  # or import from the correct path
from datetime import datetime
from django.utils import timezone
import pytz  # Ensure pytz is installed

def smartstudyhabit(request):
    # User authentication check
    if 'user_id' not in request.session:
        messages.error(request, "Please login to view your dashboard.")
        return redirect('login')

    username = request.session.get('username')
    user = userdetails.objects.get(username=username)
    students = studentdetails.objects.filter(studentname=username)

    # AI-based course recommendation
    top_course = recommend_best_course(user, COURSES, studentdetails)

    # Strengths: Courses with 85%+ completion or quiz scores >= 85
    strengths = []
    weaknesses = []
    # Quiz attempts used for additional metrics
    attempts = QuizAttempt.objects.filter(student=user)
    course_to_score = {a.coursename: (a.score or 0) for a in attempts}
    for s in students:
        # If completed or scored high in quiz
        if s.completion >= 85 or course_to_score.get(s.coursename, 0) >= 85:
            strengths.append(s.coursename)
        # If many attempts, low completion, or low score
        elif s.completion < 40 or course_to_score.get(s.coursename, 100) < 60:
            weaknesses.append(s.coursename)

    # Best study time logic: Find most frequent best hour from quiz attempts or similar logs
    best_study_time = None
    hours = []
    IST = pytz.timezone("Asia/Kolkata")
    for attempt in attempts:
        if attempt.attempted_at:
            dt = attempt.attempted_at
            if timezone.is_aware(dt):
                dt = dt.astimezone(IST)
            else:
                dt = IST.localize(dt)
            hours.append(dt.hour)
    if hours:
        from collections import Counter
        most_common_hour = Counter(hours).most_common(1)[0][0]
        best_study_time = datetime.strptime(str(most_common_hour), "%H").strftime("%I %p").lstrip("0")

    context = {
        'username': username,
        'students': students,
        'top_course': top_course,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'best_study_time': best_study_time,
        # Add messages and any extra data you want
    }
    return render(request, 'smartstudyhabit.html', context)