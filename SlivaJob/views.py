from django.http import HttpResponse

from django.shortcuts import render


def index(request):
    return render(request, 'SlivaJob/index.html')


def orders(request):
    return HttpResponse("orders")


def workers(request):
    return HttpResponse("workers")


def tests(request):
    return HttpResponse("tests")


def profile(request):
    return HttpResponse("profile")


def vacancies(request):
    return HttpResponse("vacancies")
