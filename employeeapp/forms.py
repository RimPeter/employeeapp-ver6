from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobsDone
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'validate','placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    
class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = JobsDone
        fields = ['job_title', 'job_done_in_hours']
        widgets = {
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'job_done_in_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
class CreateJobForm(forms.ModelForm):
    class Meta:
        model = JobsDone
        fields = ['job_title', 'job_done_in_hours']
        widgets = {
            'job_title': forms.Select(attrs={'class': 'form-control'}),
            'job_done_in_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        

class JobsDoneForm(forms.ModelForm):
    class Meta:
        model = JobsDone
        fields = ['job_title', 'job_done_in_hours']
