"""
Organization Permissions
Role-based permission classes for organization access
"""
from rest_framework.permissions import BasePermission


class IsOrganizationMember(BasePermission):
    """
    Permission to check if user is a member of the organization.
    """
    message = 'You must be a member of this organization.'
    
    def has_object_permission(self, request, view, obj):
        """Check if user has membership in the organization."""
        # Handle both Organization and related objects
        org = getattr(obj, 'organization', obj)
        return org.memberships.filter(user=request.user).exists()


class IsOrganizationAdmin(BasePermission):
    """
    Permission to check if user is an admin of the organization.
    """
    message = 'You must be an administrator of this organization.'
    
    def has_object_permission(self, request, view, obj):
        """Check if user is admin or owner."""
        org = getattr(obj, 'organization', obj)
        return org.memberships.filter(
            user=request.user,
            role__in=['owner', 'admin']
        ).exists()


class IsOrganizationOwner(BasePermission):
    """
    Permission to check if user is the owner of the organization.
    """
    message = 'You must be the owner of this organization.'
    
    def has_object_permission(self, request, view, obj):
        """Check if user is the owner."""
        org = getattr(obj, 'organization', obj)
        return org.owner == request.user


class HasOrganizationPermission(BasePermission):
    """
    Permission to check if user has a specific permission in the organization.
    """
    
    def __init__(self, permission: str):
        self.permission = permission
    
    def has_object_permission(self, request, view, obj):
        """Check if user has the required permission."""
        org = getattr(obj, 'organization', obj)
        try:
            membership = org.memberships.get(user=request.user)
            return membership.has_permission(self.permission)
        except org.memberships.model.DoesNotExist:
            return False
