"""
NexusCore Custom Exceptions
Domain-specific exception classes
"""
from rest_framework import status
from rest_framework.exceptions import APIException


class IdempotencyConflict(APIException):
    """
    Raised when an idempotency key is already being processed.
    Returns 409 Conflict status.
    """
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Request with this idempotency key is already being processed.'
    default_code = 'idempotency_conflict'


class IdempotencyKeyRequired(APIException):
    """
    Raised when an idempotency key is required but not provided.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Idempotency-Key header is required for this operation.'
    default_code = 'idempotency_key_required'


class RateLimitExceeded(APIException):
    """
    Raised when rate limit is exceeded.
    Returns 429 Too Many Requests status.
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Rate limit exceeded. Please try again later.'
    default_code = 'rate_limit_exceeded'


class UENValidationError(APIException):
    """
    Raised when Singapore UEN validation fails.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid Singapore Unique Entity Number (UEN).'
    default_code = 'invalid_uen'


class GSTValidationError(APIException):
    """
    Raised when GST registration number validation fails.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid GST registration number format.'
    default_code = 'invalid_gst_registration'


class OrganizationRequired(APIException):
    """
    Raised when an operation requires an organization context.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'This operation requires an organization context.'
    default_code = 'organization_required'


class InsufficientPermissions(APIException):
    """
    Raised when user lacks required permissions within an organization.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'insufficient_permissions'


class DSARSLABreached(APIException):
    """
    Raised when DSAR request exceeds 72-hour SLA (PDPA compliance).
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Data Subject Access Request SLA has been breached.'
    default_code = 'dsar_sla_breached'


class WebhookProcessingError(Exception):
    """
    Raised when webhook processing fails.
    Not an APIException as this is internal processing.
    """
    def __init__(self, service: str, event_type: str, message: str):
        self.service = service
        self.event_type = event_type
        self.message = message
        super().__init__(f"Webhook processing failed: {service}/{event_type} - {message}")


class StripeWebhookError(WebhookProcessingError):
    """Stripe-specific webhook processing error."""
    def __init__(self, event_type: str, message: str):
        super().__init__('stripe', event_type, message)
