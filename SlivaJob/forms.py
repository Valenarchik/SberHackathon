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
    status = forms.CharField(label='Выберите тип заказа', widget=forms.Select(choices=ORDER_TYPE))


class CreateOrderForm(forms.Form):
    order_name = forms.CharField(label='Название', widget=forms.TextInput())
    description = forms.CharField(label='Описание', widget=forms.Textarea())
    score = forms.IntegerField(label='Количество баллов', validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = forms.CharField(label='Комментарий', widget=forms.TextInput())


class CreateQuestionForm(forms.Form):
    question = forms.CharField(max_length=50, label="Вопрос")
    answer1 = forms.CharField(max_length=50)
    answer2 = forms.CharField(max_length=50)
    answer3 = forms.CharField(max_length=50)
    answer4 = forms.CharField(max_length=50)
    right_answer = forms.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)])

class CreateTestForm(forms.Form):
    name = forms.CharField(max_length=50, label="Название теста")