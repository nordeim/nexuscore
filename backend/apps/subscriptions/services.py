"""
Subscription Services
Business logic for subscription management
"""
from datetime import timedelta
from django.utils import timezone
from django.db import transaction

from apps.organizations.models import Organization

from .models import Plan, Subscription


class SubscriptionService:
    """Service for subscription operations."""
    
    @staticmethod
    @transaction.atomic
    def create_subscription(
        organization_id: str,
        plan_id: str,
        user,
        trial_days: int = 14
    ) -> Subscription:
        """
        Create a new subscription for an organization.
        
        Args:
            organization_id: UUID of organization
            plan_id: UUID of plan
            user: User creating the subscription
            trial_days: Number of trial days (default 14)
            
        Returns:
            Subscription: The created subscription
        """
        organization = Organization.objects.get(id=organization_id)
        plan = Plan.objects.get(id=plan_id)
        
        now = timezone.now()
        
        # Calculate period based on billing period
        if plan.billing_period == 'month':
            period_end = now + timedelta(days=30)
        else:  # year
            period_end = now + timedelta(days=365)
        
        # Create subscription
        subscription = Subscription.objects.create(
            organization=organization,
            plan=plan,
            status='trialing' if trial_days > 0 else 'active',
            current_period_start=now,
            current_period_end=period_end,
            trial_start=now if trial_days > 0 else None,
            trial_end=now + timedelta(days=trial_days) if trial_days > 0 else None,
            stripe_subscription_id=f'sub_pending_{subscription_id_placeholder()}',
            stripe_customer_id=organization.stripe_customer_id or f'cus_pending_{organization.id}',
        )
        
        # TODO: Enqueue Stripe creation task
        # from .tasks import create_stripe_subscription
        # create_stripe_subscription.delay(str(subscription.id))
        
        return subscription
    
    @staticmethod
    def upgrade_subscription(subscription: Subscription, new_plan: Plan) -> Subscription:
        """
        Upgrade a subscription to a new plan.
        
        Args:
            subscription: Current subscription
            new_plan: New plan to upgrade to
            
        Returns:
            Subscription: Updated subscription
        """
        subscription.plan = new_plan
        subscription.save(update_fields=['plan', 'updated_at'])
        
        # TODO: Update in Stripe
        # from .tasks import update_stripe_subscription
        # update_stripe_subscription.delay(str(subscription.id))
        
        return subscription
    
    @staticmethod
    def cancel_subscription(
        subscription: Subscription,
        at_period_end: bool = True
    ) -> Subscription:
        """
        Cancel a subscription.
        
        Args:
            subscription: Subscription to cancel
            at_period_end: Whether to cancel at period end
            
        Returns:
            Subscription: Updated subscription
        """
        subscription.cancel(at_period_end=at_period_end)
        
        # TODO: Cancel in Stripe
        # from .tasks import cancel_stripe_subscription
        # cancel_stripe_subscription.delay(str(subscription.id))
        
        return subscription
    
    @staticmethod
    def reactivate_subscription(subscription: Subscription) -> Subscription:
        """
        Reactivate a canceled subscription (before period end).
        
        Args:
            subscription: Subscription to reactivate
            
        Returns:
            Subscription: Updated subscription
        """
        if subscription.status != 'canceled' and subscription.cancel_at_period_end:
            subscription.cancel_at_period_end = False
            subscription.save(update_fields=['cancel_at_period_end', 'updated_at'])
        
        return subscription


def subscription_id_placeholder() -> str:
    """Generate a placeholder subscription ID."""
    import uuid
    return str(uuid.uuid4())[:8]
