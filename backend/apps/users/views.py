"""
User Views
API endpoints for user management
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    
    Endpoints:
    - GET /users/me/ - Current user profile
    - PATCH /users/me/ - Update profile
    - POST /users/me/change-password/ - Change password
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return only the current user."""
        return User.objects.filter(id=self.request.user.id)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """
        Get or update current user profile.
        
        GET: Returns current user data
        PATCH: Updates current user profile
        """
        user = request.user
        
        if request.method == 'PATCH':
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(UserSerializer(user).data)
        
        return Response(UserSerializer(user).data)
    
    @action(detail=False, methods=['post'], url_path='change-password')
    def change_password(self, request):
        """
        Change user's password.
        
        Requires:
        - current_password
        - new_password
        - new_password_confirm
        """
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Verify current password
        if not user.check_password(serializer.validated_data['current_password']):
            return Response(
                {'current_password': 'Incorrect password.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({'message': 'Password changed successfully.'})


class RegisterView(CreateAPIView):
    """
    User registration endpoint.
    
    POST /auth/register/
    
    Allows anyone to create a new account.
    Sends verification email after creation.
    """
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer
    
    def create(self, request, *args, **kwargs):
        """Create user and trigger verification email."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # TODO: Send verification email via Celery task
        # from .tasks import send_verification_email
        # send_verification_email.delay(str(user.id))
        
        return Response(
            {
                'message': 'Registration successful. Please check your email to verify your account.',
                'user': UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )


class VerifyEmailView(APIView):
    """
    Email verification endpoint.
    
    GET /auth/verify/<token>/
    
    Verifies user's email with the provided token.
    """
    permission_classes = [AllowAny]
    
    def get(self, request, token):
        """Verify email with token."""
        try:
            user = User.objects.get(verification_token=token)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid verification token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user.is_verified:
            return Response({'message': 'Email already verified.'})
        
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        
        return Response({'message': 'Email verified successfully.'})


class ResendVerificationView(APIView):
    """
    Resend verification email.
    
    POST /auth/resend-verification/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Resend verification email to current user."""
        user = request.user
        
        if user.is_verified:
            return Response(
                {'message': 'Email already verified.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.regenerate_verification_token()
        
        # TODO: Send verification email via Celery task
        # from .tasks import send_verification_email
        # send_verification_email.delay(str(user.id))
        
        return Response({'message': 'Verification email sent.'})
