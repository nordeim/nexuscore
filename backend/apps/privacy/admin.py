"""
Privacy Admin Configuration
Django admin for DSARRequest model
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import DSARRequest


@admin.register(DSARRequest)
class DSARRequestAdmin(admin.ModelAdmin):
    """Admin for DSARRequest model."""
    
    list_display = [
        'id_short',
        'user_email',
        'request_type',
        'status_badge',
        'sla_badge',
        'requires_approval',
        'is_approved',
        'requested_at',
    ]
    list_filter = [
        'request_type',
        'status',
        'requested_at',
    ]
    search_fields = [
        'user_email',
        'id',
    ]
    ordering = ['-requested_at']
    readonly_fields = [
        'id',
        'verification_token',
        'verified_at',
        'sla_status',
        'hours_remaining_in_sla',
        'requested_at',
        'processing_started_at',
        'processed_at',
    ]
    autocomplete_fields = ['user', 'deletion_approved_by']
    
    fieldsets = (
        (None, {
            'fields': ('id', 'user_email', 'user', 'request_type', 'status')
        }),
        ('SLA Tracking', {
            'fields': ('sla_status', 'hours_remaining_in_sla', 'requested_at'),
        }),
        ('Verification', {
            'fields': ('verification_token', 'verified_at', 'verification_method'),
            'classes': ('collapse',)
        }),
        ('Export', {
            'fields': ('export_url', 'export_expires_at'),
            'classes': ('collapse',)
        }),
        ('Deletion Approval', {
            'fields': ('deletion_approved_by', 'deletion_approved_at'),
            'classes': ('collapse',),
            'description': 'CRITICAL: Manual approval required for deletion requests'
        }),
        ('Processing', {
            'fields': ('processing_started_at', 'processed_at', 'failure_reason'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
    )
    
    def id_short(self, obj):
        """Show truncated ID."""
        return str(obj.id)[:8]
    id_short.short_description = 'ID'
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'pending': 'gray',
            'verifying': 'blue',
            'processing': 'orange',
            'completed': 'green',
            'failed': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def sla_badge(self, obj):
        """Display SLA status as colored badge."""
        colors = {
            'within_sla': 'green',
            'approaching_sla': 'orange',
            'breached_sla': 'red',
            'completed': 'gray',
        }
        labels = {
            'within_sla': f'OK ({obj.hours_remaining_in_sla:.1f}h)',
            'approaching_sla': f'Warning ({obj.hours_remaining_in_sla:.1f}h)',
            'breached_sla': 'BREACHED',
            'completed': 'Done',
        }
        sla = obj.sla_status
        color = colors.get(sla, 'gray')
        label = labels.get(sla, sla)
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            label
        )
    sla_badge.short_description = 'SLA'
    
    actions = ['approve_deletions']
    
    @admin.action(description='Approve selected deletion requests')
    def approve_deletions(self, request, queryset):
        """Bulk approve deletion requests."""
        approved = 0
        for dsar in queryset.filter(request_type='delete', deletion_approved_by__isnull=True):
            if dsar.is_verified:
                dsar.approve_deletion(request.user)
                approved += 1
        
        self.message_user(request, f'{approved} deletion request(s) approved.')
