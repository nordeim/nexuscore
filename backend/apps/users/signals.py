"""
User Signals
Django signals for user-related events
"""
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User
from apps.events.models import Event


@receiver(post_save, sender=User)
def user_created_handler(sender, instance, created, **kwargs):
    """
    Log user creation event for auditing.
    
    Creates an Event record when a new user is created.
    """
    if created:
        Event.log(
            event_type='user.created',
            user_id=instance.id,
            email=instance.email,
            name=instance.name,
        )


@receiver(post_save, sender=User)
def user_verified_handler(sender, instance, **kwargs):
    """
    Log user verification event.
    
    Creates an Event record when a user verifies their email.
    """
    # Check if is_verified changed to True
    if instance.is_verified:
        # Check if this is an update (not create)
        if not kwargs.get('created', False):
            try:
                old_instance = User.objects.get(pk=instance.pk)
                if not old_instance.is_verified:
                    Event.log(
                        event_type='user.verified',
                        user_id=instance.id,
                        email=instance.email,
                    )
            except User.DoesNotExist:
                pass
