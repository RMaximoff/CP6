from django.urls import path
from django.views.decorators.cache import cache_page

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'
