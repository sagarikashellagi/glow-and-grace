"""
Context processors for Glow & Grace.

These functions run on every request and inject variables into every
template. They save you from passing the same data (nav categories,
brand name, etc.) from every single view.

Registered in settings.py TEMPLATES OPTIONS context_processors list.
"""
from .models import Category


def site_context(request):
    """
    Global template context. Available in every template without
    being passed by the view.
    """
    return {
        "site_name": "Glow & Grace",
        "site_tagline": "Clean, conscious skincare for everyday radiance.",
        "nav_categories": Category.objects.all(),
    }