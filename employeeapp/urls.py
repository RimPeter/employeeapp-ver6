from django.urls import path
from . import views
from .views import clock_in_view, clock_out_view

urlpatterns = [
    path('', views.home, name=''),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-job/', views.add_job, name='add-job'),
    path('update-job/<str:pk>/', views.update_job, name='update-job'),
    path('single-job/<str:pk>/', views.single_job, name='single-job'),
    path('delete-job/<str:pk>/', views.delete_job, name='delete-job'),
    path('clockin/', clock_in_view, name='clockin'),
    path('clockout/', clock_out_view, name='clockout'),
    #path('navbar2/', views.navbar2, name='navbar2'),
    path('employee-clockin/', views.employee_clockin_view, name='employee_clockin'),
    #path('dashboard/', views.employee_clockin_view, name='employee_clockin'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]