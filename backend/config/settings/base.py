"""
NexusCore v4.0 - Base Django Settings
Singapore-first B2B SaaS Platform
Django 6.0 + PostgreSQL 16 + Redis 7.4
"""
import os
from datetime import timedelta
from pathlib import Path

from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# =============================================================================
# APPLICATION DEFINITION
# =============================================================================
INSTALLED_APPS = [
    # Django Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third Party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'django_celery_beat',
    'django_celery_results',
    'storages',
    'csp',
    
    # Local Apps (to be created in subsequent phases)
    # 'apps.core',
    # 'apps.users',
    # 'apps.organizations',
    # 'apps.subscriptions',
    # 'apps.billing',
    # 'apps.leads',
    # 'apps.privacy',
    # 'apps.webhooks',
    # 'apps.events',
]

# =============================================================================
# MIDDLEWARE
# =============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',  # Django 6.0 native CSP support
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# =============================================================================
# DATABASE (PostgreSQL 16 REQUIRED for GeneratedField)
# =============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='nexuscore'),
        'USER': config('DB_USER', default='nexuscore_user'),
        'PASSWORD': config('DB_PASSWORD', default='nexuscore_password'),
        'HOST': config('DB_HOST', default='postgres'),
        'PORT': config('DB_PORT', default='5432'),
        'CONN_HEALTH_CHECKS': True,  # Django 6.0 feature
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=5000',  # 5 second timeout
        },
    }
}

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =============================================================================
# CUSTOM USER MODEL
# =============================================================================
AUTH_USER_MODEL = 'users.User'

# =============================================================================
# PASSWORD VALIDATION
# =============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =============================================================================
# INTERNATIONALIZATION (Singapore)
# =============================================================================
LANGUAGE_CODE = 'en-sg'
TIME_ZONE = 'Asia/Singapore'
USE_I18N = True
USE_TZ = True

# =============================================================================
# STATIC FILES
# =============================================================================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# =============================================================================
# MEDIA FILES
# =============================================================================
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# AWS S3 CONFIGURATION (Singapore Region for PDPA)
# =============================================================================
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='nexuscore-storage')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='ap-southeast-1')
AWS_DEFAULT_ACL = 'private'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_QUERYSTRING_AUTH = True
AWS_S3_FILE_OVERWRITE = False

# =============================================================================
# REST FRAMEWORK
# =============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
}

# =============================================================================
# JWT CONFIGURATION
# =============================================================================
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}

# =============================================================================
# CORS CONFIGURATION
# =============================================================================
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# CSRF CONFIGURATION
# =============================================================================
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:3000,http://127.0.0.1:3000',
    cast=Csv()
)

# =============================================================================
# CELERY CONFIGURATION
# =============================================================================
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://redis:6379/1')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://redis:6379/2')
CELERY_TIMEZONE = 'Asia/Singapore'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# =============================================================================
# REDIS CACHE
# =============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': config('REDIS_URL', default='redis://redis:6379/0'),
    }
}

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='noreply@nexuscore.sg')

# =============================================================================
# CONTENT SECURITY POLICY (Django 6.0 Native)
# =============================================================================
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", 'https://js.stripe.com')
CSP_IMG_SRC = ("'self'", 'data:', 'https:')
CSP_FONT_SRC = ("'self'", 'https://fonts.gstatic.com')
CSP_CONNECT_SRC = ("'self'", 'https://api.stripe.com')
CSP_FRAME_SRC = ("'self'", 'https://js.stripe.com')

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CONTENT_TYPE_NOSNIFF = True

# =============================================================================
# STRIPE CONFIGURATION
# =============================================================================
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')
STRIPE_API_VERSION = config('STRIPE_API_VERSION', default='2024-12-18.acacia')

# =============================================================================
# SENTRY CONFIGURATION
# =============================================================================
SENTRY_DSN = config('SENTRY_DSN', default='')
SENTRY_ENVIRONMENT = config('SENTRY_ENVIRONMENT', default='development')

# =============================================================================
# PDPA COMPLIANCE (Singapore)
# =============================================================================
PDPA_DSAR_SLA_HOURS = config('PDPA_DSAR_SLA_HOURS', default=72, cast=int)
PDPA_DATA_RETENTION_DAYS = config('PDPA_DATA_RETENTION_DAYS', default=2555, cast=int)

# =============================================================================
# GST CONFIGURATION (Singapore)
# =============================================================================
from decimal import Decimal
GST_RATE = Decimal(config('GST_RATE', default='0.0900'))
GST_REGISTRATION_THRESHOLD = config('GST_REGISTRATION_THRESHOLD', default=1000000, cast=int)

# =============================================================================
# LOGGING
# =============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': config('DJANGO_LOG_LEVEL', default='INFO'),
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
