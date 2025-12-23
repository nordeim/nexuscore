"""
Organization Views
API endpoints for organization management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Organization, OrganizationMembership
from .serializers import (
    OrganizationSerializer,
    OrganizationCreateSerializer,
    OrganizationUpdateSerializer,
    OrganizationMembershipSerializer,
    InviteMemberSerializer,
)
from .permissions import IsOrganizationMember, IsOrganizationAdmin, IsOrganizationOwner

User = get_user_model()


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for organization management.
    
    Endpoints:
    - GET /organizations/ - List user's organizations
    - POST /organizations/ - Create organization
    - GET /organizations/{id}/ - Get organization details
    - PATCH /organizations/{id}/ - Update organization
    - DELETE /organizations/{id}/ - Delete organization (owner only)
    - GET /organizations/{id}/members/ - List members
    - POST /organizations/{id}/invite/ - Invite member
    - POST /organizations/{id}/remove-member/ - Remove member
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return organizations the user is a member of."""
        return Organization.objects.filter(
            memberships__user=self.request.user
        ).distinct()
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return OrganizationCreateSerializer
        if self.action in ['update', 'partial_update']:
            return OrganizationUpdateSerializer
        return OrganizationSerializer
    
    def get_permissions(self):
        """Return appropriate permissions based on action."""
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOrganizationAdmin()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsOrganizationOwner()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """
        List organization members.
        
        GET /organizations/{id}/members/
        """
        org = self.get_object()
        memberships = org.memberships.select_related('user').all()
        serializer = OrganizationMembershipSerializer(memberships, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        """
        Invite a user to the organization.
        
        POST /organizations/{id}/invite/
        
        Body:
        - email: Email of user to invite
        - role: Role to assign (admin, member, viewer)
        """
        org = self.get_object()
        
        # Check if user is admin
        try:
            membership = org.memberships.get(user=request.user)
            if not membership.is_admin:
                return Response(
                    {'error': 'Only administrators can invite members.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except OrganizationMembership.DoesNotExist:
            return Response(
                {'error': 'You are not a member of this organization.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = InviteMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        role = serializer.validated_data['role']
        
        # Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': f'No user found with email: {email}'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if already a member
        if org.memberships.filter(user=user).exists():
            return Response(
                {'error': 'User is already a member of this organization.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create membership
        membership = OrganizationMembership.objects.create(
            organization=org,
            user=user,
            role=role,
            invited_by=request.user
        )
        
        return Response(
            OrganizationMembershipSerializer(membership).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], url_path='remove-member')
    def remove_member(self, request, pk=None):
        """
        Remove a member from the organization.
        
        POST /organizations/{id}/remove-member/
        
        Body:
        - user_id: UUID of user to remove
        """
        org = self.get_object()
        
        # Check if user is admin
        try:
            requester_membership = org.memberships.get(user=request.user)
            if not requester_membership.is_admin:
                return Response(
                    {'error': 'Only administrators can remove members.'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except OrganizationMembership.DoesNotExist:
            return Response(
                {'error': 'You are not a member of this organization.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find membership
        try:
            membership = org.memberships.get(user_id=user_id)
        except OrganizationMembership.DoesNotExist:
            return Response(
                {'error': 'User is not a member of this organization.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Cannot remove owner
        if membership.role == 'owner':
            return Response(
                {'error': 'Cannot remove the organization owner.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cannot remove yourself (use leave instead)
        if membership.user == request.user:
            return Response(
                {'error': 'Use leave endpoint to remove yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        membership.delete()
        return Response({'message': 'Member removed successfully.'})
    
    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """
        Leave an organization.
        
        POST /organizations/{id}/leave/
        """
        org = self.get_object()
        
        try:
            membership = org.memberships.get(user=request.user)
        except OrganizationMembership.DoesNotExist:
            return Response(
                {'error': 'You are not a member of this organization.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Owner cannot leave
        if membership.role == 'owner':
            return Response(
                {'error': 'Owner cannot leave. Transfer ownership first.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        membership.delete()
        return Response({'message': 'You have left the organization.'})
