"""
Organization URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import OrganizationViewSet

# Router for ViewSets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')

urlpatterns = [
    path('', include(router.urls)),
]
