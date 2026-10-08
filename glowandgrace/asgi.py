"""
ASGI config for the Glow & Grace project.

It exposes the ASGI callable as a module-level variable named ``application``.

ASGI is the asynchronous sibling of WSGI — needed if you later add
WebSockets, Server-Sent Events, or async views. For a plain Django site
you won't use this file directly, but Django ships it by default so
nothing breaks if you ever run under Uvicorn, Daphne, or Hypercorn.
"""
import os

from django.core.asgi import get_asgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "glowandgrace.settings")

application = get_asgi_application()