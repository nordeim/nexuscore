"""
Lead Serializers
DRF serializers for Lead model
"""
from rest_framework import serializers

from .models import Lead


class LeadSerializer(serializers.ModelSerializer):
    """Serializer for reading lead data."""
    
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)
    is_converted = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Lead
        fields = [
            'id',
            'name',
            'email',
            'phone',
            'company',
            'job_title',
            'source',
            'status',
            'notes',
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'utm_term',
            'utm_content',
            'assigned_to',
            'assigned_to_email',
            'next_follow_up',
            'is_converted',
            'converted_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'converted_at',
        ]


class LeadCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating leads (public form submission)."""
    
    class Meta:
        model = Lead
        fields = [
            'name',
            'email',
            'phone',
            'company',
            'job_title',
            'source',
            'utm_source',
            'utm_medium',
            'utm_campaign',
            'utm_term',
            'utm_content',
            'form_data',
        ]
    
    def validate_email(self, value):
        """Normalize email to lowercase."""
        return value.lower().strip()


class LeadUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating leads (internal use)."""
    
    class Meta:
        model = Lead
        fields = [
            'status',
            'notes',
            'assigned_to',
            'next_follow_up',
        ]
