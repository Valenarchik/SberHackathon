from django.http import HttpResponse

from .forms import *

from django.shortcuts import render


def index(request):
    return render(request, 'SlivaJob/index.html')


def orders(request):
    return HttpResponse("orders")


def workers(request):
    return HttpResponse("workers")


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
