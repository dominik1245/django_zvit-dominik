"""
ASGI config for Dobre Wohnka project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dobrewohnka.settings')

application = get_asgi_application()

