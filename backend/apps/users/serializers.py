"""
User Serializers
DRF serializers for User model
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for reading user data.
    """
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'name',
            'company',
            'phone',
            'timezone',
            'is_verified',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'email',
            'is_verified',
            'created_at',
            'updated_at',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},
        help_text='Password (min 8 characters)'
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text='Confirm password'
    )
    
    class Meta:
        model = User
        fields = [
            'email',
            'name',
            'password',
            'password_confirm',
            'company',
            'phone',
        ]
    
    def validate_email(self, value):
        """Ensure email is lowercase."""
        return value.lower()
    
    def validate_password(self, value):
        """Validate password strength."""
        validate_password(value)
        return value
    
    def validate(self, attrs):
        """Ensure passwords match."""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        return attrs
    
    def create(self, validated_data):
        """Create user with hashed password."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile.
    """
    
    class Meta:
        model = User
        fields = [
            'name',
            'company',
            'phone',
            'timezone',
            'email_preferences',
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change.
    """
    current_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_new_password(self, value):
        """Validate new password strength."""
        validate_password(value)
        return value
    
    def validate(self, attrs):
        """Ensure new passwords match."""
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({
                'new_password_confirm': 'Passwords do not match.'
            })
        return attrs
