"""
Subscription Admin Configuration
Django admin for Plan and Subscription models
"""
from django.contrib import admin
from django.utils.html import format_html

from .models import Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """Admin for Plan model."""
    
    list_display = [
        'name',
        'sku',
        'formatted_price',
        'billing_period',
        'is_active',
        'is_visible',
        'display_order',
    ]
    list_filter = [
        'is_active',
        'is_visible',
        'billing_period',
        'currency',
    ]
    search_fields = ['name', 'sku', 'description']
    ordering = ['display_order', 'name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'sku')
        }),
        ('Pricing', {
            'fields': ('billing_period', 'amount_cents', 'currency')
        }),
        ('Features & Limits', {
            'fields': ('features', 'limits')
        }),
        ('Display', {
            'fields': ('is_active', 'is_visible', 'display_order')
        }),
        ('Stripe', {
            'fields': ('stripe_product_id', 'stripe_price_id'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin for Subscription model."""
    
    list_display = [
        'organization',
        'plan',
        'status_badge',
        'current_period_end',
        'cancel_at_period_end',
        'created_at',
    ]
    list_filter = [
        'status',
        'cancel_at_period_end',
        'plan',
        'created_at',
    ]
    search_fields = [
        'organization__name',
        'organization__uen',
        'stripe_subscription_id',
    ]
    ordering = ['-created_at']
    readonly_fields = [
        'created_at',
        'updated_at',
        'canceled_at',
        'stripe_subscription_id',
        'stripe_customer_id',
    ]
    autocomplete_fields = ['organization', 'plan']
    
    fieldsets = (
        (None, {
            'fields': ('organization', 'plan', 'status')
        }),
        ('Period', {
            'fields': ('current_period_start', 'current_period_end', 'cancel_at_period_end')
        }),
        ('Trial', {
            'fields': ('trial_start', 'trial_end')
        }),
        ('Stripe', {
            'fields': ('stripe_subscription_id', 'stripe_customer_id', 'stripe_latest_invoice_id'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'canceled_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'trialing': 'blue',
            'active': 'green',
            'past_due': 'orange',
            'canceled': 'red',
            'unpaid': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
