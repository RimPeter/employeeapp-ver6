from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name=''),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('add-job/', views.add_job, name='add-job'),
    path('update-job/<str:pk>/', views.update_job, name='update-job'),
    path('single-job/<str:pk>/', views.single_job, name='single-job'),
]