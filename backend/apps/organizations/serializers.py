"""
Organization Serializers
DRF serializers for Organization and Membership models
"""
from rest_framework import serializers
from django.utils.text import slugify

from .models import Organization, OrganizationMembership


class OrganizationMembershipSerializer(serializers.ModelSerializer):
    """Serializer for organization memberships."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    
    class Meta:
        model = OrganizationMembership
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'role',
            'permissions',
            'joined_at',
        ]
        read_only_fields = ['id', 'joined_at']


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for reading organization data."""
    
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    is_in_trial = serializers.BooleanField(read_only=True)
    days_left_in_trial = serializers.IntegerField(read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = [
            'id',
            'name',
            'slug',
            'uen',
            'is_gst_registered',
            'gst_reg_no',
            'billing_email',
            'billing_phone',
            'timezone',
            'locale',
            'owner',
            'owner_email',
            'is_in_trial',
            'days_left_in_trial',
            'member_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'slug',
            'owner',
            'created_at',
            'updated_at',
        ]
    
    def get_member_count(self, obj) -> int:
        """Get number of members in organization."""
        return obj.memberships.count()


class OrganizationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating organizations."""
    
    class Meta:
        model = Organization
        fields = [
            'name',
            'uen',
            'is_gst_registered',
            'gst_reg_no',
            'billing_email',
            'billing_phone',
            'billing_address',
            'timezone',
            'locale',
        ]
    
    def validate_uen(self, value):
        """Ensure UEN is uppercase."""
        return value.upper().strip()
    
    def validate_gst_reg_no(self, value):
        """Ensure GST reg no is uppercase."""
        if value:
            return value.upper().strip()
        return value
    
    def validate(self, attrs):
        """Validate GST registration consistency."""
        is_gst_registered = attrs.get('is_gst_registered', False)
        gst_reg_no = attrs.get('gst_reg_no')
        
        if is_gst_registered and not gst_reg_no:
            raise serializers.ValidationError({
                'gst_reg_no': 'GST registration number is required for GST-registered organizations.'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Create organization with owner as first member."""
        request = self.context.get('request')
        validated_data['owner'] = request.user
        validated_data['slug'] = slugify(validated_data['name'])
        
        org = Organization.objects.create(**validated_data)
        
        # Add owner as first member
        OrganizationMembership.objects.create(
            organization=org,
            user=request.user,
            role='owner'
        )
        
        return org


class OrganizationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating organizations."""
    
    class Meta:
        model = Organization
        fields = [
            'name',
            'is_gst_registered',
            'gst_reg_no',
            'billing_email',
            'billing_phone',
            'billing_address',
            'timezone',
            'locale',
            'settings',
        ]


class InviteMemberSerializer(serializers.Serializer):
    """Serializer for inviting members."""
    
    email = serializers.EmailField()
    role = serializers.ChoiceField(
        choices=['admin', 'member', 'viewer'],
        default='member'
    )
    
    def validate_email(self, value):
        """Normalize email to lowercase."""
        return value.lower().strip()
