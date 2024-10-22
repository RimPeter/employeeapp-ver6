"""
Module Overview.

This module contains custom form classes for user creation,
user login, job record management, and employee clock-in and
clock-out functionalities within a Django application.
"""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import JobsDone, ClockIn, Profile, Employee
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.core.exceptions import ValidationError


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


class ClockInForm(forms.Form):
    pass

class ClockOutForm(forms.ModelForm):
    """Clock out an employee."""

    class Meta:
        """Specify the model and fields for the clock-out form."""

        model = ClockIn
        fields = ['employee']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'phone_number', 'email_address']
        
        # Customize widgets (optional)
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    # Optional: Add extra validation for phone number or other fields if needed
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if len(phone) < 10:  # Example: Validate phone number length
            raise ValidationError("Phone number must be at least 10 digits long.")
        return phone