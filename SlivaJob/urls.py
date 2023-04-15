from django.urls import path, include
from SberHackathon import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('to_employee/', to_employee, name='to_employee'),
    path('to_employee/success_post', success_post, name='success_post'),
    path('to_employee/orders/', orders, name='orders'),
    path('to_employee/tests/', tests, name='tests'),
    path('to_employee/test/<int:test_id>/', test, name='test'),
    path('to_employer/', to_employer, name='to_employer'),
    path('to_mentor/', to_mentor, name='to_mentor'),
    path('to_mentor/create_test/', create_test, name='create_test'),
    path('to_mentor/my_tests/', my_tests, name='my_tests'),
    path('to_orderer/', to_orderer, name='to_orderer'),
    path('to_orderer/create_order/', create_order, name='create_order'),
    path('workers/', workers, name='workers'),
    path('profile/', profile, name='profile'),
    path('vacancies/', vacancies, name='vacancies'),
    path('sign_up/', sign_up, name='sign_up'),
    path('log_in/', log_in, name='log_in'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
