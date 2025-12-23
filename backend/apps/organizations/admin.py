"""
Organization Admin Configuration
Django admin for Organization and Membership models
"""
from django.contrib import admin
from .models import Organization, OrganizationMembership


class OrganizationMembershipInline(admin.TabularInline):
    """Inline for organization memberships."""
    model = OrganizationMembership
    extra = 0
    readonly_fields = ['joined_at']
    autocomplete_fields = ['user', 'invited_by']


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin for Organization model."""
    
    list_display = [
        'name',
        'uen',
        'is_gst_registered',
        'owner',
        'member_count',
        'is_in_trial',
        'created_at',
    ]
    list_filter = [
        'is_gst_registered',
        'org_timezone',
        'created_at',
    ]
    search_fields = ['name', 'uen', 'billing_email']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['owner']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrganizationMembershipInline]
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'owner')
        }),
        ('Singapore Compliance', {
            'fields': ('uen', 'is_gst_registered', 'gst_reg_no'),
            'description': 'UEN and GST registration details'
        }),
        ('Billing', {
            'fields': ('stripe_customer_id', 'billing_email', 'billing_phone', 'billing_address')
        }),
        ('Settings', {
            'fields': ('timezone', 'locale', 'settings')
        }),
        ('Trial', {
            'fields': ('trial_ends_at',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def member_count(self, obj):
        """Display member count."""
        return obj.memberships.count()
    member_count.short_description = 'Members'


@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):
    """Admin for OrganizationMembership model."""
    
    list_display = ['user', 'organization', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']
    search_fields = ['user__email', 'organization__name']
    autocomplete_fields = ['user', 'organization', 'invited_by']
    readonly_fields = ['joined_at']
