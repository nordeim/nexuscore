"""
Subscriptions App Configuration
"""
from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    """Subscriptions application configuration."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.subscriptions'
    verbose_name = 'Subscriptions'
