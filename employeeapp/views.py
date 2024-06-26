from django.shortcuts import render
from django.http import HttpResponse

def employee(request):
    return HttpResponse("Hello, There!")