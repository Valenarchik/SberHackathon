from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'surname', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'surname': forms.TextInput(attrs={'class': 'form-input'}),
            'password': forms.PasswordInput(attrs={'class': 'form-input'})
        }


class LogInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-input'})
        }


class ProfileForm(forms.ModelForm):
    model = User
    fields = ('first_name', 'surname', 'photo')
    widgets = {
        'first_name': forms.TextInput(attrs={'class': 'form-input'}),
        'surname': forms.TextInput(attrs={'class': 'form-input'}),
        'photo': forms.FileInput(attrs={'class': 'file-input'})
    }