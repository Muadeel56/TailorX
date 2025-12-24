from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import MeasurementTemplate, CustomerMeasurement
from .serializers import (
    MeasurementTemplateSerializer,
    CustomerMeasurementSerializer,
    CustomerMeasurementCreateSerializer
)


class MeasurementTemplateListView(generics.ListAPIView):
    """List all measurement templates."""

    queryset = MeasurementTemplate.objects.all()
    serializer_class = MeasurementTemplateSerializer
    permission_classes = (AllowAny,)


class MeasurementTemplateDetailView(generics.RetrieveAPIView):
    """Get detailed information about a measurement template."""

    queryset = MeasurementTemplate.objects.all()
    serializer_class = MeasurementTemplateSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'id'


class CustomerMeasurementListView(generics.ListCreateAPIView):
    """List user's measurements or create a new measurement."""

    serializer_class = CustomerMeasurementSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return only the authenticated user's measurements."""
        return CustomerMeasurement.objects.filter(
            customer=self.request.user
        ).select_related('template', 'customer')

    def get_serializer_class(self):
        """Use different serializer for creation."""
        if self.request.method == 'POST':
            return CustomerMeasurementCreateSerializer
        return CustomerMeasurementSerializer

    def perform_create(self, serializer):
        """Set the customer to the authenticated user."""
        serializer.save(customer=self.request.user)


class CustomerMeasurementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Get, update, or delete a specific measurement."""

    serializer_class = CustomerMeasurementSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        """Return only the authenticated user's measurements."""
        return CustomerMeasurement.objects.filter(
            customer=self.request.user
        ).select_related('template', 'customer')
