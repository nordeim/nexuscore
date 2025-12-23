"""
Webhook Admin Configuration
Django admin for WebhookEvent model
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import WebhookEvent


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    """Admin for WebhookEvent model."""
    
    list_display = [
        'event_id_short',
        'service',
        'event_type',
        'processed_badge',
        'retry_count',
        'created_at',
        'processed_at',
    ]
    list_filter = [
        'service',
        'processed',
        'event_type',
        'created_at',
    ]
    search_fields = [
        'event_id',
        'event_type',
    ]
    ordering = ['-created_at']
    readonly_fields = [
        'id',
        'event_id',
        'payload',
        'created_at',
        'processed_at',
    ]
    
    fieldsets = (
        (None, {
            'fields': ('id', 'service', 'event_id', 'event_type', 'processed')
        }),
        ('Processing', {
            'fields': ('retry_count', 'processing_error', 'created_at', 'processed_at')
        }),
        ('Payload', {
            'fields': ('payload',),
            'classes': ('collapse',)
        }),
    )
    
    def event_id_short(self, obj):
        """Show truncated event ID."""
        if obj.event_id:
            return obj.event_id[:20] + '...' if len(obj.event_id) > 20 else obj.event_id
        return '-'
    event_id_short.short_description = 'Event ID'
    
    def processed_badge(self, obj):
        """Display processed status as colored badge."""
        if obj.processed:
            return format_html('<span style="color: green;">✓ Processed</span>')
        else:
            return format_html('<span style="color: orange;">Pending</span>')
    processed_badge.short_description = 'Status'
    
    actions = ['retry_failed']
    
    @admin.action(description='Retry failed webhook events')
    def retry_failed(self, request, queryset):
        """Retry failed webhook events."""
        from .tasks import process_stripe_webhook
        
        retried = 0
        for event in queryset.filter(processed=False, service='stripe'):
            process_stripe_webhook.delay(str(event.id))
            retried += 1
        
        self.message_user(request, f'{retried} webhook event(s) queued for retry.')

