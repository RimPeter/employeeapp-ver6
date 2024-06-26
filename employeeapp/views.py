"""
Module Overview.

This module contains view functions for handling
various operations in the Employee App,
including user registration, login, logout, job record management,
and employee clock-in and clock-out functionalities.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UpdateJobForm, ClockInForm, ClockOutForm
from .forms import LoginForm, CustomUserCreationForm, JobsDoneForm
from .models import JobsDone, ClockIn, Employee


def home(request):
    """Render the home page."""
    return render(request, 'employeeapp/index.html')


def register(request):
    """Handle user registration."""
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account has been created successfully!")
            return redirect('login')
    context = {'form': form}
    return render(request, 'employeeapp/register.html', context=context)


def login(request):
    """Handle user login."""
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context = {'form': form}
    return render(request, 'employeeapp/login.html', context=context)


def logout(request):
    """Handle user logout."""
    auth.logout(request)
    messages.success(request, "Logout successful!")
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """Render the dashboard page with job records."""
    job_done = JobsDone.objects.all()
    context = {'job_done': job_done}
    return render(request, 'employeeapp/dashboard.html', context=context)


@login_required(login_url='login')
def dashboard_view(request):
    """Render the dashboard page with job records, employees, and clock-ins."""
    job_done = JobsDone.objects.all()
    employees = Employee.objects.all()
    clockins = ClockIn.objects.select_related('employee').all()
    context = {
        'job_done': job_done,
        'employees': employees,
        'clockins': clockins,
    }
    return render(request, 'employeeapp/dashboard.html', context)


@login_required(login_url='login')
def add_job(request):
    """Handle adding a new job record."""
    if request.method == 'POST':
        form = JobsDoneForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.worker = request.user
            job.save()
            messages.success(request, "Your job-record has been created!")
            return redirect('dashboard')
    else:
        form = JobsDoneForm()
    context = {'form': form}
    return render(request, 'employeeapp/create-record.html', context)


@login_required(login_url='login')
def update_job(request, pk):
    """Handle updating an existing job record."""
    job = JobsDone.objects.get(id=pk)
    form = UpdateJobForm(instance=job)
    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Your job-record has been updated!")
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'employeeapp/update-record.html', context=context)


@login_required(login_url='login')
def single_job(request, pk):
    """Display a single job record."""
    jobdone = JobsDone.objects.get(id=pk)
    context = {'jobdone': jobdone}
    return render(request, 'employeeapp/view-record.html', context=context)


@login_required(login_url='login')
def delete_job(request, pk):
    """Handle deleting a job record."""
    job = JobsDone.objects.get(id=pk)
    job.delete()
    messages.info(request, 'Job has been deleted!')
    return redirect('dashboard')


@login_required(login_url='login')
@staff_member_required
def clock_in_view(request):
    """Handle clocking in of employees."""
    if request.method == 'POST':
        form = ClockInForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Clock-in successful!')
            return redirect('admin:index')
    else:
        form = ClockInForm()
    return render(request, 'employeeapp/clockin.html', {'form': form})


@login_required(login_url='login')
@staff_member_required
def clock_out_view(request):
    """Handle clocking out of employees."""
    if request.method == 'POST':
        form = ClockOutForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            clock_in_instance = ClockIn.objects.filter(
                employee=employee, clock_out_time__isnull=True).first()
            if clock_in_instance:
                clock_in_instance.clock_out_time = timezone.now()
                clock_in_instance.save()
                messages.info(request, 'Clock-out successful!')
                return redirect('admin:index')
    else:
        form = ClockOutForm()
    return render(request, 'employeeapp/clockout.html', {'form': form})


@login_required(login_url='login')
def employee_clockin_view(request):
    """Display clock-in records of all employees."""
    employees = Employee.objects.all()
    clockins = ClockIn.objects.select_related('employee').all()
    context = {
        'employees': employees,
        'clockins': clockins,
    }
    return render(request, 'employeeapp/employee-clockin.html', context)
