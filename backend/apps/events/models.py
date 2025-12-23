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
    
    Note: user_id and organization_id are stored as UUIDs.
    In Phase 3+, we'll add proper ForeignKey relationships via migrations.
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
    
    # Related entities - stored as UUIDs until User/Organization apps exist
    # These will be converted to ForeignKeys in Phase 3/4 via migration
    user_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
        help_text='UUID of the user who triggered the event'
    )
    organization_id = models.UUIDField(
        null=True,
        blank=True,
        db_index=True,
        help_text='UUID of the organization context'
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
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['organization_id', 'created_at']),
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
        import uuid as uuid_module
        
        user_id = getattr(user, 'id', None) if user else None
        org_id = getattr(organization, 'id', None) if organization else None
        
        # Convert any UUID values in data to strings for JSON serialization
        serialized_data = {}
        for key, value in data.items():
            if isinstance(value, uuid_module.UUID):
                serialized_data[key] = str(value)
            else:
                serialized_data[key] = value
        
        return cls.objects.create(
            event_type=event_type,
            user_id=user_id,
            organization_id=org_id,
            data=serialized_data
        )
