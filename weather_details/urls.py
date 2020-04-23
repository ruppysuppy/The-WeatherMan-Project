# imports from django
from django.urls import path

# local imports
from .views import about, home, details

# url patterns registration
urlpatterns = [
    path('about/', about, name='about'),
    path('', home, name='home'),
    path('details/', details, name='details'),
]