"""
URL patterns for the 'products' app.

Mounted at / by the root urlconf, so:

  ''                          → home
  'about/'                    → about
  'products/'                 → products list
  'products/<slug>/'          → single product detail
  'faq/'                      → faq
  'contact/'                  → contact
  'newsletter/subscribe/'     → newsletter signup (POST)
  'privacy-policy/'           → privacy policy
  'terms/'                    → terms & conditions

The namespace 'products' lets templates reverse these by name, e.g.
{% url 'products:detail' slug=product.slug %}
"""
from django.urls import path

from . import views


app_name = "products"


urlpatterns = [
    # Home
    path("", views.home, name="home"),

    # Products
    path("products/", views.products_list, name="list"),
    path("products/<slug:slug>/", views.product_detail, name="detail"),

    # Informational pages
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),

    # Newsletter (POST endpoint, no standalone page)
    path(
        "newsletter/subscribe/",
        views.newsletter_subscribe,
        name="newsletter_subscribe",
    ),

    # Legal
    path("privacy-policy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]