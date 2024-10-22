"""
Module Overview.

This module contains view functions for handling
various operations in the Employee App,
including user registration, login, logout, job record management,
and employee clock-in and clock-out functionalities.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .forms import UpdateJobForm, ClockInForm, ClockOutForm, ProfileForm
from .forms import LoginForm, CustomUserCreationForm, JobsDoneForm
from .models import JobsDone, ClockIn, Employee, Profile
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
import logging

def home(request):
    """Render the home page."""
    return render(request, 'employeeapp/index.html')


def register(request):
    """Handle user registration."""
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        password = request.POST.get('password1')  

        if len(password) < 8:  # Check if password is less than 8 characters
            messages.error(request, "Password must be at least 8 characters long.")
        elif form.is_valid():
            form.save()
            messages.success(request, "Account has been created successfully!")
            return redirect('login')
        else:
            messages.error(request, "There was an error with your registration. Please try again.")
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
                messages.success(request, "Login successful!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
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
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None
    if request.method == 'POST':
        form = JobsDoneForm(request.POST)
        if form.is_valid() and profile is not None:
            job = form.save(commit=False)
            job.worker = request.user
            job.save()
            messages.success(request, "Your job-record has been created!")
            return redirect('dashboard')
        else:
            if profile is None:
                messages.error(request, "There was an error with the job submission. Please try again.")
            else:
                messages.error(request, "There was an error with the job submission. Please try again.")
    else:
        form = JobsDoneForm()
    context = {
        'form': form,
        'profile': profile,
        }
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
        else:
            messages.error(request, "There was an error updating the job. Please try again.")
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
def clock_in_view(request):
    try:
        profile = request.user.profile
    except ObjectDoesNotExist:
        profile = None

    try:
        employee = Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, "Your account is not associated with an employee profile yet.")
        return redirect('create_profile')

    if not profile:
        messages.error(request, "You must complete your profile before clocking in.")
        return redirect('create_profile')

    # Check if the user is already clocked in
    active_clockin = ClockIn.objects.filter(employee=employee, clock_out_time__isnull=True).first()

    if request.method == 'POST':
        if active_clockin:
            # User wants to clock out
            active_clockin.clock_out_time = timezone.now()
            active_clockin.save()
            messages.success(request, "You have successfully clocked out.")
            return redirect('clock_out_success')
        else:
            # User wants to clock in
            form = ClockInForm(request.POST)
            if form.is_valid():
                clock_in = ClockIn.objects.create(employee=employee)
                messages.success(request, "You have successfully clocked in.")
                return redirect('clock_in_success')
            else:
                messages.error(request, "There was an error with clock-in. Please try again.")
                return render(request, 'employeeapp/clockin.html', {'form': form, 'profile': profile})
    else:
        if active_clockin:
            # User is clocked in; display clock-out option
            return render(request, 'employeeapp/clockin.html', {'active_clockin': active_clockin, 'profile': profile})
        else:
            # User is not clocked in; display clock-in form
            form = ClockInForm()
            return render(request, 'employeeapp/clockin.html', {'form': form, 'profile': profile})

@login_required(login_url='login')
def clock_in_success(request):
    """Render a success message after clocking in."""
    clock_in_time = timezone.now()
    return render(request, 'employeeapp/clock_in_success.html', {'clock_in_time': clock_in_time})

@login_required(login_url='login')
def clock_out_success(request):
    """Render a success message after clocking out."""
    clock_out_time = timezone.now()
    return render(request, 'employeeapp/clock_out_success.html', {'clock_out_time': clock_out_time})

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
                messages.error(request, 'No active clock-in found for this employee.')
        else:
            messages.error(request, "Form is invalid. Please try again.")
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

@login_required(login_url='login')
def create_profile(request):
    """Handle profile creation."""
    try:
        profile = request.user.profile
        messages.info(request, "You already have a profile.")
        return redirect('profile_detail', pk=profile.pk)
    except Profile.DoesNotExist:
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, 'Profile created successfully!')
                return redirect('profile_detail', pk=profile.pk) 
            else:
                messages.error(request, 'There was an error creating the profile.')
        else:
            form = ProfileForm()
        
        context = {'form': form}
        return render(request, 'employeeapp/create_profile.html', context)

@login_required(login_url='login')
def edit_profile(request, pk):
    """Handle profile update."""
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile_detail', pk=profile.pk) 
        else:
            messages.error(request, 'There was an error updating the profile.')
    else:
        form = ProfileForm(instance=profile)
    
    context = {'form': form, 'profile': profile}
    return render(request, 'employeeapp/edit_profile.html', context)

def profile_detail(request, pk):
    """Display profile details."""
    profile = get_object_or_404(Profile, pk=pk)
    context = {'profile': profile}
    return render(request, 'employeeapp/profile_detail.html', context)

@login_required
def delete_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)

    if profile.user != request.user:
        messages.error(request, "You are not authorized to delete this profile.")
        return redirect('profile_detail', pk=profile.pk)

    if request.method == 'POST':
        profile.delete()
        messages.success(request, "Your profile has been deleted.")
        return redirect('dashboard')  

    return render(request, 'employeeapp/delete_profile.html', {'profile': profile})

@login_required
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Ensure that the user is the logged-in user
    if user != request.user:
        messages.error(request, "You are not authorized to delete this account.")
        return redirect('profile_detail', pk=request.user.profile.pk)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('login')  # Redirect to the home page after account deletion

    return render(request, 'employeeapp/delete_user.html', {'user': user})

logger = logging.getLogger(__name__)
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    View to handle password change.
    """
    template_name = 'employeeapp/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        logger.info(f"User {self.request.user.username} is changing their password.")
        messages.success(self.request, "Your password was successfully updated!")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"User {self.request.user.username} failed to change their password.")
        messages.error(self.request, "There was an error changing your password. Please try again.")
        return super().form_invalid(form)

class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    """
    View to confirm password change.
    """
    template_name = 'employeeapp/password_change_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Password Change Successful"
        return context

    def get(self, request, *args, **kwargs):
        logger.info(f"User {request.user.username} has successfully changed their password.")
        return super().get(request, *args, **kwargs)
    

