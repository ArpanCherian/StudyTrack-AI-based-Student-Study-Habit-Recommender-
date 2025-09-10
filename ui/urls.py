from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registration_view, name='register'),
    path('home/', views.index_view, name='index'),
]