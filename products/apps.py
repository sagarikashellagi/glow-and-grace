"""
App configuration for the 'products' app.

Django reads this class on startup to register the app. The
`verbose_name` shows up in the admin sidebar; `default_auto_field`
sets what `AutoField` primary keys use — modern Django projects use
BigAutoField (64-bit integers) to avoid running out of IDs.
"""
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"
    verbose_name = "Shop"