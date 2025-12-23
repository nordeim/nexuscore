"""
NexusCore URL Configuration
API versioned at /api/v1/
"""
from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def health_check(request):
    """Health check endpoint for container orchestration."""
    return JsonResponse({
        'status': 'healthy',
        'service': 'nexuscore-backend',
        'version': '4.0.0',
    })


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Health Check
    path('health/', health_check, name='health_check'),
    
    # API v1
    path('api/v1/', include('apps.users.urls')),
    path('api/v1/', include('apps.organizations.urls')),
    path('api/v1/', include('apps.subscriptions.urls')),
    path('api/v1/', include('apps.billing.urls')),
    path('api/v1/', include('apps.leads.urls')),
    path('api/v1/', include('apps.privacy.urls')),
    
    # Webhooks (no /api/v1 prefix)
    path('', include('apps.webhooks.urls')),
]

# Debug toolbar URLs (only in development)
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

