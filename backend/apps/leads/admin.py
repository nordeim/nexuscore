"""
Lead Admin Configuration
Django admin for Lead model
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    """Admin for Lead model."""
    
    list_display = [
        'name',
        'email',
        'company',
        'source',
        'status_badge',
        'assigned_to',
        'created_at',
    ]
    list_filter = [
        'source',
        'status',
        'assigned_to',
        'created_at',
    ]
    search_fields = [
        'name',
        'email',
        'company',
        'phone',
    ]
    ordering = ['-created_at']
    readonly_fields = [
        'created_at',
        'updated_at',
        'converted_at',
    ]
    autocomplete_fields = ['assigned_to', 'converted_to_user']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'email', 'phone', 'company', 'job_title')
        }),
        ('Lead Management', {
            'fields': ('source', 'status', 'notes', 'assigned_to', 'next_follow_up')
        }),
        ('UTM Tracking', {
            'fields': ('utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'),
            'classes': ('collapse',)
        }),
        ('Form Data', {
            'fields': ('form_data',),
            'classes': ('collapse',)
        }),
        ('Conversion', {
            'fields': ('converted_to_user', 'converted_at'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'new': 'blue',
            'contacted': 'orange',
            'qualified': 'purple',
            'converted': 'green',
            'disqualified': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
