from django.urls import path, include
from SberHackathon import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('to_employee/', to_employee, name='to_employee'),
    path('to_employer/', to_employer, name='to_employer'),
    path('to_mentor/', to_mentor, name='to_mentor'),
    path('to_orderer/', to_orderer, name='to_orderer'),
    path('orders/', orders, name='orders'),
    path('workers/', workers, name='workers'),
    path('tests/', tests, name='tests'),
    path('profile/', profile, name='profile'),
    path('vacancies/', vacancies, name='vacancies'),
    path('sign_up/', sign_up, name='sign_up'),
    path('test/<int:test_id>', test, name='test'),
    path('log_in/', log_in, name='log_in'),
    #Станица для тестов сайта
    path('test_page', test_page)
    #

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
