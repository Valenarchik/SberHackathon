from django.http import HttpResponse

from .forms import *
from .models import *

from django.shortcuts import render


def index(request):
    context ={}
    if request.COOKIES.get('is_log_in') == "1":
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
    http.set_cookie()
    return http


def sign_up(request):
    html_page = None
    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            context = {'is_log_in': True}
            sign_up_form.save()
            html_page = render(request, 'SlivaJob/index.html', context)
            html_page.set_cookie('is_log_in', '1', max_age=None)
        else:
            context = {'sing_up_form': sign_up_form}
            html_page = render(request, 'SlivaJob/signup.html', context)
    else:
        sign_up_form = SignUpForm()
        context = {'sing_up_form': sign_up_form}
        html_page = render(request, 'SlivaJob/signup.html',context )
    return html_page


def profile(request):
    return render(request, 'SlivaJob/profile.html')


def vacancies(request):
    return render(request, 'SlivaJob/vacancies.html')
