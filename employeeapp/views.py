from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'employeeapp/index.html')
    #return HttpResponse("Hello, world. You're at the employeeapp index.")