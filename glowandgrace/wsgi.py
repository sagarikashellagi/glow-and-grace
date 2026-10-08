"""
WSGI config for the Glow & Grace project.

It exposes the WSGI callable as a module-level variable named ``application``.

This is the file Gunicorn loads on Render:
    gunicorn glowandgrace.wsgi:application
"""
import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glowandgrace.settings")

application = get_wsgi_application()