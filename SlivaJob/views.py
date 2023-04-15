from django.http import HttpResponse

from .forms import *

from django.shortcuts import render


def index(request):
    return render(request, 'SlivaJob/index.html')


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

    if request.method == 'POST':
        sign_up_form = SignUpForm(request.POST)
        # if sing_up_form.is_valid():
        #     None
    else:
        sign_up_form = SignUpForm()
    context['sing_up_form'] = sign_up_form
    return render(request, 'SlivaJob/test.html', context)


def profile(request):
    return HttpResponse("profile")


def vacancies(request):
    return HttpResponse("vacancies")
