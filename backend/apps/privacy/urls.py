"""
Privacy URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DSARRequestViewSet

# Router for ViewSets
router = DefaultRouter()
router.register(r'dsar', DSARRequestViewSet, basename='dsar')

urlpatterns = [
    path('', include(router.urls)),
]
