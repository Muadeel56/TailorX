from rest_framework import serializers
from .models import TailorProfile
from users.serializers import UserSerializer


class TailorListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for tailor list view."""
    user = UserSerializer(read_only=True)
    specialization_display = serializers.CharField(
        source='get_specialization_display',
        read_only=True
    )
    availability_status_display = serializers.CharField(
        source='get_availability_status_display',
        read_only=True
    )
    
    class Meta:
        model = TailorProfile
        fields = (
            'id', 'user', 'shop_name', 'specialization', 
            'specialization_display', 'experience_years', 
            'rating', 'total_reviews', 'availability_status',
            'availability_status_display', 'latitude', 'longitude'
        )


class TailorDetailSerializer(serializers.ModelSerializer):
    """Full serializer for tailor detail view."""
    user = UserSerializer(read_only=True)
    specialization_display = serializers.CharField(
        source='get_specialization_display',
        read_only=True
    )
    availability_status_display = serializers.CharField(
        source='get_availability_status_display',
        read_only=True
    )
    
    class Meta:
        model = TailorProfile
        fields = (
            'id', 'user', 'shop_name', 'shop_address', 
            'specialization', 'specialization_display',
            'experience_years', 'rating', 'total_reviews',
            'bio', 'portfolio_images', 'availability_status',
            'availability_status_display', 'latitude', 'longitude',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class TailorPortfolioSerializer(serializers.Serializer):
    """Serializer for portfolio images."""
    portfolio_images = serializers.ListField(
        child=serializers.CharField(),
        read_only=True
    )

