from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'surname', 'email', 'password')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input '}),
            'surname': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.TextInput(attrs={'class': 'email-input'}),
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
    class Meta:
        model = User
        fields = ('first_name', 'surname')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'surname': forms.TextInput(attrs={'class': 'form-input'}),
            # 'email': forms.EmailField(attrs={'class': 'email-input'}),
        }


ORDER_TYPE = [
    ('-1', 'Все'),
    ('0', 'Активные'),
    ('1', 'В процессе выполнения'),
    ('2', 'Выполненные'),
]


class FilterOrderForm(forms.Form):
    score = forms.CharField(label='Выберите тип заказа', widget=forms.Select(choices=ORDER_TYPE))


class CreateOrderForm(forms.Form):
    order_name = forms.CharField(widget=forms.TextInput())
    description = forms.CharField(widget=forms.Textarea())
    score = forms.CharField(label='Выберите тип заказа', widget=forms.Select(choices=ORDER_TYPE))
    comment = forms.CharField(widget=forms.TextInput())
