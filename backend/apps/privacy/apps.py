"""
Privacy App Configuration
"""
from django.apps import AppConfig


class PrivacyConfig(AppConfig):
    """Privacy application configuration."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.privacy'
    verbose_name = 'Privacy'
