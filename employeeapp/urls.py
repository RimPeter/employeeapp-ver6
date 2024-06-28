from django.urls import path
from . import views

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
    path('clock-in/', views.clock_in, name='clock-in'),
    path('clock-out/', views.clock_out, name='clock-out'),
]