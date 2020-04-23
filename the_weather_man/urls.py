# Importing Third Party Packages

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URL Pattern Base (Extended in weather_details.urls)

urlpatterns = [
    path('', include('weather_details.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
