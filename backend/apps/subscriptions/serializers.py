"""
Subscription Serializers
DRF serializers for Plan and Subscription models
"""
from rest_framework import serializers

from .models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    """Serializer for reading plan data."""
    
    amount_dollars = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    formatted_price = serializers.CharField(read_only=True)
    
    class Meta:
        model = Plan
        fields = [
            'id',
            'name',
            'description',
            'sku',
            'billing_period',
            'amount_cents',
            'amount_dollars',
            'currency',
            'features',
            'limits',
            'is_active',
            'is_visible',
            'display_order',
            'formatted_price',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for reading subscription data."""
    
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_in_trial = serializers.BooleanField(read_only=True)
    days_until_renewal = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Subscription
        fields = [
            'id',
            'organization',
            'organization_name',
            'plan',
            'plan_name',
            'status',
            'cancel_at_period_end',
            'current_period_start',
            'current_period_end',
            'trial_start',
            'trial_end',
            'is_active',
            'is_in_trial',
            'days_until_renewal',
            'created_at',
            'canceled_at',
        ]
        read_only_fields = [
            'id',
            'status',
            'current_period_start',
            'current_period_end',
            'created_at',
            'canceled_at',
        ]


class SubscriptionCreateSerializer(serializers.Serializer):
    """Serializer for creating subscriptions."""
    
    organization_id = serializers.UUIDField()
    plan_id = serializers.UUIDField()
    
    def validate_organization_id(self, value):
        """Validate organization exists and user has access."""
        from apps.organizations.models import Organization
        
        request = self.context.get('request')
        try:
            org = Organization.objects.get(id=value)
        except Organization.DoesNotExist:
            raise serializers.ValidationError('Organization not found.')
        
        # Check user is admin of org
        if not org.memberships.filter(user=request.user, role__in=['owner', 'admin']).exists():
            raise serializers.ValidationError('You must be an admin to manage subscriptions.')
        
        return value
    
    def validate_plan_id(self, value):
        """Validate plan exists and is active."""
        try:
            plan = Plan.objects.get(id=value, is_active=True)
        except Plan.DoesNotExist:
            raise serializers.ValidationError('Plan not found or not available.')
        return value


class CancelSubscriptionSerializer(serializers.Serializer):
    """Serializer for canceling subscriptions."""
    
    at_period_end = serializers.BooleanField(default=True)
