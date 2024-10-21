"""
Module Overview.

This module contains custom form classes for user creation,
user login, job record management, and employee clock-in and
clock-out functionalities within a Django application.
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobsDone, ClockIn
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class CustomUserCreationForm(UserCreationForm):
    """Create a new user with custom styling."""

    class Meta:
        """Specify the model and fields for the user creation form."""

        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }


class LoginForm(AuthenticationForm):
    """Log in a user with custom styling."""

    username = forms.CharField(widget=TextInput(attrs={
        'class': 'validate', 'placeholder': 'Username'}))
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Password'}))


class UpdateJobForm(forms.ModelForm):
    """Update an existing job record."""

    class Meta:
        """Specify the model and fields for updating a job record."""

        model = JobsDone
        fields = ['job_title', 'job_done_in_hours']


class CreateJobForm(forms.ModelForm):
    """Create a new job record with custom styling."""

    class Meta:
        """Specify the model, fields, and widgets for creating a job record."""

        model = JobsDone
        fields = ['job_title', 'job_done_in_hours']
        widgets = {
            'job_title': forms.Select(attrs={
                'class': 'form-control'}),
            'job_done_in_hours': forms.NumberInput(attrs={
                'class': 'form-control'}),
        }


class JobsDoneForm(forms.ModelForm):
    """Handle job records."""

    class Meta:
        """Specify the model and fields for the job record form."""

        model = JobsDone
        fields = ['job_title', 'job_done_in_hours']


class ClockInForm(forms.ModelForm):
    """Clock in an employee."""

    class Meta:
        """Specify the model and fields for the clock-in form."""

        model = ClockIn
        fields = []
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ClockInForm, self).__init__(*args, **kwargs)
        if user and user.is_superuser:
            # Superusers can select any employee
            self.fields['employee'] = forms.ModelChoiceField(
                queryset=User.objects.all(),
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=True
            )


class ClockOutForm(forms.ModelForm):
    """Clock out an employee."""

    class Meta:
        """Specify the model and fields for the clock-out form."""

        model = ClockIn
        fields = ['employee']
