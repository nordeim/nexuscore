"""
User Celery Tasks
Background tasks for email and user operations
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


@shared_task(queue='default')
def send_verification_email(user_id: str) -> None:
    """
    Send email verification link to user.
    
    Args:
        user_id: UUID of the user to send verification to
    """
    from .models import User
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return
    
    if user.is_verified:
        return
    
    verification_url = f"{settings.SITE_URL}/verify/{user.verification_token}/"
    
    subject = 'Verify your NexusCore account'
    message = f"""
    Hi {user.name},
    
    Please verify your email address by clicking the link below:
    
    {verification_url}
    
    This link will expire in 24 hours.
    
    If you didn't create an account, please ignore this email.
    
    Best regards,
    The NexusCore Team
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


@shared_task(queue='default')
def send_welcome_email(user_id: str) -> None:
    """
    Send welcome email after user verification.
    
    Args:
        user_id: UUID of the user to welcome
    """
    from .models import User
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return
    
    subject = 'Welcome to NexusCore!'
    message = f"""
    Hi {user.name},
    
    Welcome to NexusCore! Your account has been verified and you're ready to go.
    
    Get started by:
    1. Creating your first organization
    2. Inviting team members
    3. Setting up your subscription
    
    If you need any help, our support team is here for you.
    
    Best regards,
    The NexusCore Team
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


@shared_task(queue='default')
def send_password_reset_email(user_id: str, token: str) -> None:
    """
    Send password reset link to user.
    
    Args:
        user_id: UUID of the user
        token: Password reset token
    """
    from .models import User
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return
    
    reset_url = f"{settings.SITE_URL}/reset-password/{token}/"
    
    subject = 'Reset your NexusCore password'
    message = f"""
    Hi {user.name},
    
    We received a request to reset your password. Click the link below:
    
    {reset_url}
    
    This link will expire in 1 hour.
    
    If you didn't request a password reset, please ignore this email.
    
    Best regards,
    The NexusCore Team
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )
