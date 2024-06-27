from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from employeeapp.forms import LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from .models import JobsDone

def home(request):
    return render(request, 'employeeapp/index.html')

def login(request):
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
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    job_done = JobsDone.objects.all()
    context = {'job_done': job_done}
    return render(request, 'employeeapp/dashboard.html', context=context)

@login_required(login_url='login')
def add_job(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        job_done_in_hours = request.POST.get('job_done_in_hours')
        JobsDone.objects.create(worker=request.user, job_title=job_title, job_done_in_hours=job_done_in_hours)
        return redirect('dashboard')
    return render(request, 'employeeapp/create-record.html')

@login_required(login_url='login')
def update_job(request, pk):
    job = JobsDone.objects.get(id=pk)
    form = JobsDone(instance=job)
    if request.method == 'POST':
        form = JobsDone(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'employeeapp/update-record.html', context=context)

@login_required(login_url='login')
def single_job(request, pk):
    all_jobs = JobsDone.objects.get(id=pk)
    context = {'all_jobs': all_jobs}
    return render(request, 'employeeapp/view-record.html', context=context)


