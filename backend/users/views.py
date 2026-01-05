from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.core.cache import cache
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """List all users (Admin only)."""
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser)
    queryset = User.objects.all().order_by('-date_joined')

    def get_queryset(self):
        """Return all users with optional filtering."""
        queryset = super().get_queryset()
        
        # Filter by user type if provided
        user_type = self.request.query_params.get('user_type', None)
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        
        # Search by email or name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                email__icontains=search
            ) | queryset.filter(
                full_name__icontains=search
            )
        
        return queryset


class PasswordResetRequestView(generics.GenericAPIView):
    """Request password reset - generates reset token."""
    serializer_class = PasswordResetRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return success even if user doesn't exist (security best practice)
            return Response({
                'message': 'If this email exists, a password reset token has been generated.',
                'note': 'In production, this would be sent via email.'
            }, status=status.HTTP_200_OK)
        
        # Generate reset token (32 character random string)
        reset_token = get_random_string(32)
        
        # Store token in cache with 1 hour expiration
        cache_key = f'password_reset_{user.id}'
        cache.set(cache_key, reset_token, timeout=3600)  # 1 hour
        
        # In development, return token in response
        # In production, send via email
        return Response({
            'message': 'Password reset token generated successfully.',
            'reset_token': reset_token,  # Remove this in production
            'email': email,
            'note': 'In production, this token would be sent via email. Store it securely.',
            'expires_in': '1 hour'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    """Confirm password reset with token."""
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        reset_token = serializer.validated_data['reset_token']
        new_password = serializer.validated_data['new_password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid email or reset token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify reset token
        cache_key = f'password_reset_{user.id}'
        stored_token = cache.get(cache_key)
        
        if not stored_token or stored_token != reset_token:
            return Response(
                {'error': 'Invalid or expired reset token.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Reset password
        user.set_password(new_password)
        user.save()
        
        # Delete used token
        cache.delete(cache_key)
        
        return Response({
            'message': 'Password has been reset successfully. You can now login with your new password.'
        }, status=status.HTTP_200_OK)
