"""
User Admin Configuration
Django admin for User model
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for custom User model.
    """
    
    # List display
    list_display = [
        'email',
        'name',
        'company',
        'is_verified_badge',
        'is_active',
        'is_staff',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'is_staff',
        'is_superuser',
        'is_verified',
        'created_at',
    ]
    search_fields = ['email', 'name', 'company']
    ordering = ['-created_at']
    
    # Form fieldsets
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('name', 'company', 'phone', 'timezone')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_token', 'verification_sent_at')
        }),
        ('Preferences', {
            'fields': ('email_preferences',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    # Add form fieldsets
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at', 'last_login', 'verification_token']
    
    def is_verified_badge(self, obj):
        """Display verification status as badge."""
        if obj.is_verified:
            return format_html(
                '<span style="color: green;">✓ Verified</span>'
            )
        return format_html(
            '<span style="color: orange;">○ Pending</span>'
        )
    is_verified_badge.short_description = 'Verified'
