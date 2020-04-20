from django.contrib import admin
from django.urls import path

from .views import about, home, details

urlpatterns = [
    path('about/', about, name='about'),
    path('', home, name='home'),
    path('details/', details, name='details'),
]