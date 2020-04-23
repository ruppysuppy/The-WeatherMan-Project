# django imports

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# url patterns, for the site
urlpatterns = [
    path('', include('weather_details.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
