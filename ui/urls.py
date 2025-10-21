from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registration_view, name='register'),
    path('home/', views.index_view, name='index'),
    path('userdashboard/',views.userdashboard,name='userdashboard'),
    path('logout/', views.index_view, name='logout'),
    path('studysessions/', views.studysessions, name='studysessions'),
    path('admindashboard/', views.admindashboard, name='admindashboard'),
    path('adminlogin/', views.adminlogin_view, name='adminlogin'),
    path('newstudent/', views.newstudent_view, name='newstudent'),
    path('add_student_view/', views.add_student_view, name='addstudent'),
    path('studentcourses/', views.studentcourses, name='studentcourses'),
    path('ongoing_course/', views.ongoing_course, name='ongoing_course'),
    path('send_course_reminder/', views.send_course_reminder, name='send_course_reminder'),
    path('usernotification/', views.usernotification, name='usernotification'),
]