"""
Privacy Serializers
DRF serializers for DSARRequest model
"""
from rest_framework import serializers

from .models import DSARRequest


class DSARRequestSerializer(serializers.ModelSerializer):
    """Serializer for reading DSAR request data."""
    
    sla_status = serializers.CharField(read_only=True)
    hours_remaining_in_sla = serializers.FloatField(read_only=True)
    is_verified = serializers.BooleanField(read_only=True)
    requires_approval = serializers.BooleanField(read_only=True)
    is_approved = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = DSARRequest
        fields = [
            'id',
            'user_email',
            'request_type',
            'status',
            'sla_status',
            'hours_remaining_in_sla',
            'is_verified',
            'verified_at',
            'requires_approval',
            'is_approved',
            'deletion_approved_at',
            'export_url',
            'export_expires_at',
            'requested_at',
            'processed_at',
        ]
        read_only_fields = [
            'id',
            'status',
            'verified_at',
            'deletion_approved_at',
            'export_url',
            'export_expires_at',
            'requested_at',
            'processed_at',
        ]


class DSARRequestCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating DSAR requests (public)."""
    
    class Meta:
        model = DSARRequest
        fields = [
            'user_email',
            'request_type',
        ]
    
    def validate_user_email(self, value):
        """Normalize email."""
        return value.lower().strip()


class DSARVerifySerializer(serializers.Serializer):
    """Serializer for verifying DSAR requests."""
    
    token = serializers.UUIDField()


class DSARApproveDeleteSerializer(serializers.Serializer):
    """Serializer for approving deletion requests."""
    
    confirmation = serializers.CharField()
    
    def validate_confirmation(self, value):
        """Require explicit confirmation."""
        if value != 'CONFIRM_DELETE':
            raise serializers.ValidationError(
                "Must pass 'CONFIRM_DELETE' to approve deletion."
            )
        return value
