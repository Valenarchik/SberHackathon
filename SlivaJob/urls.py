from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('orders', orders, name='orders'),
    path('workers', workers, name='workers'),
    path('tests', tests, name='test'),
    path('profile', profile, name='profile'),
    path('vacancies', vacancies, name='vacancies'),

]
