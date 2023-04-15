from django.http import HttpResponse

from .forms import *
from .models import *

from django.shortcuts import render,redirect


def index(request):
    context ={}
    if request.COOKIES.get('id'):
        context['is_log_in'] = True
    else:
        context['is_log_in'] = False

    return render(request, 'SlivaJob/index.html', context)


def orders(request):
    context = {
        "ordersList": Order.objects.all()
    }
    return render(request, 'SlivaJob/orders.html', context=context)


def workers(request):
    workersList = Worker.objects.all()
    usersList = [User.objects.get(pk=w.worker_id) for w in workersList]
    context = {
        "workersList": zip(workersList, usersList)
    }
    return render(request, 'SlivaJob/workers.html', context=context)


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
            user = sign_up_form.save()
            html_page = redirect('index')
            html_page.set_cookie('id', f'{user.id}', max_age=None)
        else:
            context = {'sing_up_form': sign_up_form}
            html_page = render(request, 'SlivaJob/signup.html', context)
    else:
        sign_up_form = SignUpForm()
        context = {'sing_up_form': sign_up_form}
        html_page = render(request, 'SlivaJob/signup.html',context )
    return html_page


def profile(request):
    context = {}
    html_page = None
    id = request.COOKIES.get('id')
    if id:
        id = int(id)
        form = ProfileForm(User.objects.get(id=id))
        context['profile_form'] = form
        html_page = render(request, 'SlivaJob/profile.html', context);
    else:
        html_page = redirect('index')
    return html_page


def vacancies(request):
    return render(request, 'SlivaJob/vacancies.html')
