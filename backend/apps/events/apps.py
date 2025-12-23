"""
Events App Configuration
"""
from django.apps import AppConfig


class EventsConfig(AppConfig):
    """Events application configuration."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.events'
    verbose_name = 'Events'
