from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from .forms import LoginForm, CustomUserCreationForm, JobsDoneForm, UpdateJobForm, ClockInForm, ClockOutForm
from .models import JobsDone, ClockIn


def home(request):
    return render(request, 'employeeapp/index.html')

def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'employeeapp/register.html', context=context)

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
        form = JobsDoneForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.worker = request.user
            job.save()
            return redirect('dashboard')
    else:
        form = JobsDoneForm()
    context = {'form': form}
    return render(request, 'employeeapp/create-record.html', context)


@login_required(login_url='login')
def update_job(request, pk):
    job = JobsDone.objects.get(id=pk)
    form = UpdateJobForm(instance=job)
    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context = {'form': form}
    return render(request, 'employeeapp/update-record.html', context=context)

@login_required(login_url='login')
def single_job(request, pk):
    jobdone = JobsDone.objects.get(id=pk)
    context = {'jobdone': jobdone}
    return render(request, 'employeeapp/view-record.html', context=context)


@login_required(login_url='login')
def delete_job(request, pk):
    job = JobsDone.objects.get(id=pk)
    job.delete()
    messages.info(request, 'Job Deleted')
    return redirect('dashboard')


@login_required(login_url='login')
@staff_member_required
def clock_in_view(request):
    if request.method == 'POST':
        form = ClockInForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:index')
    else:
        form = ClockInForm()
    return render(request, 'employeeapp/clockin.html', {'form': form})

@login_required(login_url='login')
@staff_member_required
def clock_out_view(request):
    if request.method == 'POST':
        form = ClockOutForm(request.POST)
        if form.is_valid():
            employee = form.cleaned_data['employee']
            clock_in_instance = ClockIn.objects.filter(employee=employee, clock_out_time__isnull=True).first()
            if clock_in_instance:
                clock_in_instance.clock_out_time = timezone.now()
                clock_in_instance.save()
                return redirect('admin:index')
    else:
        form = ClockOutForm()
    return render(request, 'employeeapp/clockout.html', {'form': form})

# @login_required(login_url='login')
# @staff_member_required
# def clock_in_list(request):
#     clock_in_list = ClockIn.objects.all()
#     context = {'clock_in_list': clock_in_list}
#     return render(request, 'employeeapp/clockin.html', context=context)

@login_required(login_url='login')
def clockin_list(request):
    clock_in_list = ClockIn.objects.all()
    context = {'clock_in_list': clock_in_list}
    return render(request, 'employeeapp/dashboard.html', context=context)