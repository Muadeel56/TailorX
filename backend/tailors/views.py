from rest_framework import generics, filters
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import TailorProfile
from .serializers import (
    TailorListSerializer, 
    TailorDetailSerializer,
    TailorPortfolioSerializer
)


class TailorListView(generics.ListAPIView):
    """List all tailors with filtering and search."""
    queryset = TailorProfile.objects.all()
    serializer_class = TailorListSerializer
    permission_classes = (AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['specialization', 'availability_status']
    search_fields = ['shop_name', 'user__full_name']
    ordering_fields = ['rating', 'experience_years', 'created_at']
    ordering = ['-rating', '-total_reviews']  # Default ordering
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by minimum rating
        min_rating = self.request.query_params.get('min_rating', None)
        if min_rating:
            try:
                queryset = queryset.filter(rating__gte=float(min_rating))
            except ValueError:
                pass
        
        return queryset


class TailorDetailView(generics.RetrieveAPIView):
    """Get detailed information about a specific tailor."""
    queryset = TailorProfile.objects.all()
    serializer_class = TailorDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'id'


class TailorPortfolioView(generics.RetrieveAPIView):
    """Get portfolio images for a specific tailor."""
    queryset = TailorProfile.objects.all()
    serializer_class = TailorPortfolioSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'id'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer({
            'portfolio_images': instance.portfolio_images or []
        })
        return Response(serializer.data)
