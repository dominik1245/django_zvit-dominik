"""
WSGI config for Dobre Wohnka project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dobrewohnka.settings')

application = get_wsgi_application()

