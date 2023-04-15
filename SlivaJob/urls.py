from django.urls import path, include
from SberHackathon import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('orders', orders, name='orders'),
    path('workers', workers, name='workers'),
    path('tests', tests, name='tests'),
    path('profile', profile, name='profile'),
    path('vacancies', vacancies, name='vacancies'),
    path('sign_up', sign_up, name='sign_up'),
    path('login', login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
