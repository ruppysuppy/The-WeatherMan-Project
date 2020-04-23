import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'the_weather_man.settings')

application = get_wsgi_application()
