from django import forms
from .models import *


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
             'password': forms.PasswordInput(),
        }


class LogInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['login', '']