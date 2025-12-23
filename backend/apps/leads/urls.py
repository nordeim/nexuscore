"""
Leads URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LeadViewSet

# Router for ViewSets
router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')

urlpatterns = [
    path('', include(router.urls)),
]
