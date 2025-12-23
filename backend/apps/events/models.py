"""
Event Model
Audit logging for all mutations (PRD-d-3)
"""
import uuid
from django.db import models


class Event(models.Model):
    """
    System event for analytics and auditing.
    
    Tracks all significant actions in the system for:
    - Audit compliance
    - Analytics
    - Debugging
    - Activity feeds
    
    Note: ForeignKeys use string references since User and Organization
    models will be created in later phases.
    """
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Event type (e.g., 'user.created', 'subscription.activated')
    event_type = models.CharField(
        max_length=100,
        db_index=True,
        help_text='Event type in dot notation (e.g., user.created)'
    )
    
    # Related entities (nullable - will be resolved when models exist)
    user = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text='User who triggered the event'
    )
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
        help_text='Organization context for the event'
    )
    
    # Event data
    data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Event payload data'
    )
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['event_type', 'created_at']),
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['organization', 'created_at']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Event: {self.event_type} at {self.created_at}"
    
    @classmethod
    def log(cls, event_type: str, user=None, organization=None, **data):
        """
        Convenience method to create an event.
        
        Usage:
            Event.log('user.created', user=user, email=user.email)
            Event.log('subscription.activated', organization=org, plan_id=plan.id)
        """
        return cls.objects.create(
            event_type=event_type,
            user=user,
            organization=organization,
            data=data
        )
