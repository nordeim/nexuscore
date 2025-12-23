"""
NexusCore URL Configuration
API versioned at /api/v1/
"""
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
    
    # Future API modules (Phase 4+)
    # path('api/v1/organizations/', include('apps.organizations.urls')),
]
