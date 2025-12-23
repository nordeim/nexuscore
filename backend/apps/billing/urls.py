"""
Billing URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet

# Router for ViewSets
router = DefaultRouter()
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]
