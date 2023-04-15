from django.urls import path, include
from SberHackathon import settings
from django.conf.urls.static import static

from SlivaJob.views import *

urlpatterns = [
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

