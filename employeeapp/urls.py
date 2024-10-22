"""
Module Overview.

This module defines URL patterns for routing HTTP requests to
appropriate view functions within the Employee App. It imports
necessary modules and view functions to handle various functionalities
such as user registration, login, job management,
and employee clock-in and clock-out.
"""

from django.urls import path
from . import views
from .views import clock_in_view, clock_out_view
from django.contrib.auth import views as auth_views
from .views import clock_in_view, clock_out_view, CustomPasswordChangeView, CustomPasswordChangeDoneView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-job/', views.add_job, name='add-job'),
    path('update-job/<str:pk>/', views.update_job, name='update-job'),
    path('single-job/<str:pk>/', views.single_job, name='single-job'),
    path('delete-job/<str:pk>/', views.delete_job, name='delete-job'),
    path('clockin/', clock_in_view, name='employee-clockin'),
    path('clockout/', clock_out_view, name='clockout'),
    #path('dashboard/', views.employee_clockin_view, name='dashboard'),
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/<int:pk>/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:pk>/delete/', views.delete_profile, name='delete_profile'),
    path('user/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('password_change/', 
         CustomPasswordChangeView.as_view(), 
         name='password_change'),
    
    path('password_change/done/', 
         CustomPasswordChangeDoneView.as_view(), 
         name='password_change_done'),
]
