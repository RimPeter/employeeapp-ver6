from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from employeeapp.forms import LoginForm
from django.contrib.auth.models import auth


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
                login(request, user)
                return redirect('home')
    context = {'form': form}
    return render(request, 'employeeapp/login.html', context=context) 