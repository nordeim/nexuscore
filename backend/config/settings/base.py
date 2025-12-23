"""
NexusCore v4.0 - Base Django Settings
Singapore-first B2B SaaS Platform
Django 6.0 + PostgreSQL 16 + Redis 7.4
"""
import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


def get_env(key, default=None, cast=str):
    """Helper function to get environment variables with type casting."""
    value = os.environ.get(key, default)
    if value is None:
        return None
    if cast == bool:
        return value.lower() in ('true', '1', 'yes', 'on')
    if cast == int:
        return int(value)
    if cast == list:
        return [v.strip() for v in value.split(',') if v.strip()]
    return value


# =============================================================================
# SECURITY SETTINGS
# =============================================================================
SECRET_KEY = get_env('SECRET_KEY', 'django-insecure-change-me-in-production')
DEBUG = get_env('DEBUG', 'False', cast=bool)
ALLOWED_HOSTS = get_env('ALLOWED_HOSTS', 'localhost,127.0.0.1', cast=list)

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
    'django.contrib.postgres',  # Required for ArrayField
    
    # Third Party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'django_celery_beat',
    'django_celery_results',
    'storages',
    'csp',
    
    # Local Apps - Phase 2: Infrastructure
    'apps.core',
    'apps.billing',
    'apps.events',
    'apps.webhooks',
    
    # Local Apps - Phase 3: User & Auth
    'apps.users',
    
    # Local Apps - Phase 4: Organization
    'apps.organizations',
    
    # Local Apps - Phase 5+: To be enabled
    # 'apps.subscriptions',
    # 'apps.leads',
    # 'apps.privacy',
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
    'csp.middleware.CSPMiddleware',
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
        'NAME': get_env('DB_NAME', 'nexuscore'),
        'USER': get_env('DB_USER', 'nexuscore_user'),
        'PASSWORD': get_env('DB_PASSWORD', 'nexuscore_password'),
        'HOST': get_env('DB_HOST', 'localhost'),
        'PORT': get_env('DB_PORT', '5432'),
        'CONN_HEALTH_CHECKS': True,
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'connect_timeout': 10,
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
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

# =============================================================================
# MEDIA FILES
# =============================================================================
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =============================================================================
# AWS S3 CONFIGURATION (Singapore Region for PDPA)
# =============================================================================
AWS_ACCESS_KEY_ID = get_env('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = get_env('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = get_env('AWS_STORAGE_BUCKET_NAME', 'nexuscore-storage')
AWS_S3_REGION_NAME = get_env('AWS_S3_REGION_NAME', 'ap-southeast-1')
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
CORS_ALLOWED_ORIGINS = get_env(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000',
    cast=list
)
CORS_ALLOW_CREDENTIALS = True

# =============================================================================
# CSRF CONFIGURATION
# =============================================================================
CSRF_TRUSTED_ORIGINS = get_env(
    'CSRF_TRUSTED_ORIGINS',
    'http://localhost:3000,http://127.0.0.1:3000',
    cast=list
)

# =============================================================================
# CELERY CONFIGURATION
# =============================================================================
CELERY_BROKER_URL = get_env('CELERY_BROKER_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = get_env('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
CELERY_TIMEZONE = 'Asia/Singapore'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# =============================================================================
# REDIS CACHE
# =============================================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': get_env('REDIS_URL', 'redis://localhost:6379/0'),
    }
}

# =============================================================================
# EMAIL CONFIGURATION
# =============================================================================
EMAIL_BACKEND = get_env('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = get_env('EMAIL_HOST', 'localhost')
EMAIL_PORT = get_env('EMAIL_PORT', '25', cast=int)
EMAIL_USE_TLS = get_env('EMAIL_USE_TLS', 'False', cast=bool)
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = get_env('DEFAULT_FROM_EMAIL', 'noreply@nexuscore.sg')

# =============================================================================
# CONTENT SECURITY POLICY (django-csp 4.0 format)
# =============================================================================
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'style-src': ("'self'", "'unsafe-inline'"),
        'script-src': ("'self'", "'unsafe-inline'", "'unsafe-eval'", 'https://js.stripe.com'),
        'img-src': ("'self'", 'data:', 'https:'),
        'font-src': ("'self'", 'https://fonts.gstatic.com'),
        'connect-src': ("'self'", 'https://api.stripe.com'),
        'frame-src': ("'self'", 'https://js.stripe.com'),
    }
}

# =============================================================================
# SECURITY SETTINGS
# =============================================================================
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CONTENT_TYPE_NOSNIFF = True

# =============================================================================
# STRIPE CONFIGURATION
# =============================================================================
STRIPE_PUBLIC_KEY = get_env('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = get_env('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = get_env('STRIPE_WEBHOOK_SECRET', '')
STRIPE_API_VERSION = get_env('STRIPE_API_VERSION', '2024-12-18.acacia')

# =============================================================================
# SENTRY CONFIGURATION
# =============================================================================
SENTRY_DSN = get_env('SENTRY_DSN', '')
SENTRY_ENVIRONMENT = get_env('SENTRY_ENVIRONMENT', 'development')

# =============================================================================
# PDPA COMPLIANCE (Singapore)
# =============================================================================
PDPA_DSAR_SLA_HOURS = get_env('PDPA_DSAR_SLA_HOURS', '72', cast=int)
PDPA_DATA_RETENTION_DAYS = get_env('PDPA_DATA_RETENTION_DAYS', '2555', cast=int)

# =============================================================================
# GST CONFIGURATION (Singapore)
# =============================================================================
from decimal import Decimal
GST_RATE = Decimal(get_env('GST_RATE', '0.0900'))
GST_REGISTRATION_THRESHOLD = get_env('GST_REGISTRATION_THRESHOLD', '1000000', cast=int)

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
            'level': get_env('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'apps': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
