from django.shortcuts import render, redirect
from .forms import *


def index(request):
    context = {}
    if request.COOKIES.get('id'):
        context['is_log_in'] = True
    else:
        context['is_log_in'] = False

    return render(request, 'SlivaJob/index.html', context)


def orders(request):
    return render(request, 'SlivaJob/orders.html')


def workers(request):
    return render(request, 'SlivaJob/workers.html')


def tests(request):
    context = {}
    http = render(request, 'SlivaJob/test.html', context)
    return http


def sign_up(request):
    html_page = None
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            user = sign_up_form.save()
            html_page = redirect('index')
            html_page.set_cookie('id', f'{user.id}', max_age=None)
        else:
            context = {'sing_up_form': sign_up_form}
            html_page = render(request, 'SlivaJob/signup.html', context)
    else:
        sign_up_form = SignUpForm()
        context = {'sing_up_form': sign_up_form}
        html_page = render(request, 'SlivaJob/signup.html', context)
    return html_page


def log_in(request):
    html_page = None
    if request.method == 'POST':
        log_in_form = LogInForm(request.POST)
        if log_in_form.is_valid():
            email = log_in_form.cleaned_data['email']
            password = log_in_form.cleaned_data['password']
            user = User.objects.get(email=email)
            if user:
                if user.password == password:
                    html_page = redirect('index')
                    html_page.set_cookie('id', f'{user.id}', max_age=None)
                else:
                    context = {'log_in_form': log_in_form}
                    html_page = render(request, 'SlivaJob/login.html', context)
                    log_in_form.add_error('password', 'Неверный пароль')
            else:
                log_in_form.add_error('email', 'Указан неверный E-mail')
    else:
        log_in_form = LogInForm()

    if html_page is None:
        context = {'log_in_form': log_in_form}
        html_page = render(request, 'SlivaJob/login.html', context)
    return html_page


def profile(request):
    context = {}
    id = request.COOKIES.get('id')
    if id:
        user = User.objects.get(id=int(id))
        if request.POST:
            form = ProfileForm(request.POST, instance=user)
            form.save()
        else:
            form = ProfileForm(instance=user)
        context['profile_form'] = form
        html_page = render(request, 'SlivaJob/profile.html', context)
    else:
        html_page = redirect('index')
    return html_page


def vacancies(request):
    return render(request, 'SlivaJob/vacancies.html')


import django_filters


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = User
        fields = ['price', 'release_date']
