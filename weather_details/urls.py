# Importing Third Party Packages

from django.urls import path

# Local Imports

from .views import about, home, details

# Url Patterns Registration

urlpatterns = [
    path('about/', about, name='about'),
    path('', home, name='home'),
    path('details/', details, name='details'),
]