"""
NexusCore v4.0 - Development Settings
Extends base.py with development-specific overrides
"""
from .base import *  # noqa: F401, F403

# =============================================================================
# DEVELOPMENT OVERRIDES
# =============================================================================
DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# =============================================================================
# EMAIL - Use Mailpit for development
# =============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mailpit'
EMAIL_PORT = 1025
EMAIL_USE_TLS = False

# =============================================================================
# CELERY - Eager execution for development
# =============================================================================
# Uncomment to run tasks synchronously for debugging
# CELERY_TASK_ALWAYS_EAGER = True

# =============================================================================
# SECURITY - Relaxed for development
# =============================================================================
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
