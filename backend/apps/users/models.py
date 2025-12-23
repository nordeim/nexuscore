"""
Custom User Model
Email-based authentication with UUID primary key
"""
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with email as the username field.
    
    Features:
    - UUID primary key
    - Email-based authentication
    - Singapore timezone default
    - Email verification support
    """
    
    # Primary key
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    
    # Authentication
    email = models.EmailField(
        unique=True,
        db_index=True,
        help_text='Email address used for login'
    )
    
    # Profile
    name = models.CharField(
        max_length=255,
        help_text='Full name'
    )
    company = models.CharField(
        max_length=255,
        blank=True,
        help_text='Company name'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text='Phone number'
    )
    
    # Preferences
    timezone = models.CharField(
        max_length=50,
        default='Asia/Singapore',
        help_text='User timezone'
    )
    email_preferences = models.JSONField(
        default=dict,
        blank=True,
        help_text='Email notification preferences'
    )
    
    # Email verification
    is_verified = models.BooleanField(
        default=False,
        help_text='Whether email has been verified'
    )
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        help_text='Token for email verification'
    )
    verification_sent_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When verification email was sent'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        help_text='Whether user can login'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Whether user can access admin'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    # Manager
    objects = UserManager()
    
    # Auth configuration
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
        constraints = [
            # Verified users must be active
            models.CheckConstraint(
                condition=models.Q(is_verified=False) | models.Q(is_active=True),
                name='verified_users_must_be_active'
            )
        ]
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
            models.Index(fields=['is_active', 'is_verified']),
        ]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the user's full name."""
        return self.name
    
    def get_short_name(self):
        """Return the user's short name (first name)."""
        return self.name.split()[0] if self.name else self.email
    
    def regenerate_verification_token(self):
        """Generate a new verification token."""
        self.verification_token = uuid.uuid4()
        self.verification_sent_at = timezone.now()
        self.save(update_fields=['verification_token', 'verification_sent_at'])
        return self.verification_token
    
    def verify_email(self, token):
        """
        Verify user's email with the provided token.
        
        Args:
            token: UUID token from verification email
            
        Returns:
            bool: True if verification successful
        """
        if str(self.verification_token) == str(token):
            self.is_verified = True
            self.save(update_fields=['is_verified'])
            return True
        return False
