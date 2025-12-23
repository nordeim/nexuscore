"""
NexusCore Validators
Singapore-specific validation for UEN and GST
"""
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# =============================================================================
# UEN (Unique Entity Number) Validation
# Singapore ACRA formats:
# - 8 digits + 1 letter (e.g., 12345678A)
# - 9 digits + 1 letter (e.g., 123456789A)
# - T/S/R/Q + 2 digits + 4 alphanumeric + 1 letter (e.g., T12AB123A)
# =============================================================================

UEN_REGEX = r'^[0-9]{8}[A-Z]$|^[0-9]{9}[A-Z]$|^[TSRQ][0-9]{2}[A-Z0-9]{4}[0-9]{3}[A-Z]$'

UENValidator = RegexValidator(
    regex=UEN_REGEX,
    message='Enter a valid Singapore UEN. Valid formats: 12345678A, 123456789A, or T12AB123A.',
    code='invalid_uen'
)


def validate_uen(value: str) -> None:
    """
    Validate Singapore Unique Entity Number (UEN).
    
    Args:
        value: The UEN string to validate
        
    Raises:
        ValidationError: If the UEN format is invalid
    """
    if not value:
        raise ValidationError('UEN is required.', code='required')
    
    # Normalize to uppercase
    value = value.upper().strip()
    
    if not re.match(UEN_REGEX, value):
        raise ValidationError(
            'Enter a valid Singapore UEN. Valid formats: 12345678A, 123456789A, or T12AB123A.',
            code='invalid_uen'
        )


# =============================================================================
# GST Registration Number Validation
# Singapore IRAS format: M + 8 digits + 1 letter (e.g., M12345678A)
# =============================================================================

GST_REG_NO_REGEX = r'^M[0-9]{8}[A-Z]$'

GSTRegNoValidator = RegexValidator(
    regex=GST_REG_NO_REGEX,
    message='Enter a valid GST registration number. Format: M12345678A.',
    code='invalid_gst_registration'
)


def validate_gst_reg_no(value: str) -> None:
    """
    Validate Singapore GST registration number.
    
    Args:
        value: The GST registration number to validate
        
    Raises:
        ValidationError: If the GST registration format is invalid
    """
    if not value:
        return  # GST registration is optional
    
    # Normalize to uppercase
    value = value.upper().strip()
    
    if not re.match(GST_REG_NO_REGEX, value):
        raise ValidationError(
            'Enter a valid GST registration number. Format: M12345678A.',
            code='invalid_gst_registration'
        )


# =============================================================================
# Phone Number Validation (Singapore)
# =============================================================================

SG_PHONE_REGEX = r'^\+65[689]\d{7}$|^[689]\d{7}$'

SGPhoneValidator = RegexValidator(
    regex=SG_PHONE_REGEX,
    message='Enter a valid Singapore phone number.',
    code='invalid_sg_phone'
)


def validate_sg_phone(value: str) -> None:
    """
    Validate Singapore phone number.
    
    Args:
        value: The phone number to validate
        
    Raises:
        ValidationError: If the phone format is invalid
    """
    if not value:
        return  # Phone is optional
    
    # Remove spaces and dashes
    value = re.sub(r'[\s\-]', '', value)
    
    if not re.match(SG_PHONE_REGEX, value):
        raise ValidationError(
            'Enter a valid Singapore phone number.',
            code='invalid_sg_phone'
        )
