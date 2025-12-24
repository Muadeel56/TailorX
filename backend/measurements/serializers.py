from rest_framework import serializers
from .models import MeasurementTemplate, CustomerMeasurement


class MeasurementTemplateSerializer(serializers.ModelSerializer):
    """Serializer for measurement templates."""

    measurement_type_display = serializers.CharField(
        source='get_measurement_type_display',
        read_only=True
    )

    class Meta:
        model = MeasurementTemplate
        fields = (
            'id', 'name', 'description', 'measurement_type',
            'measurement_type_display', 'standard_measurements',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class CustomerMeasurementSerializer(serializers.ModelSerializer):
    """Serializer for customer measurements with template details."""

    template = MeasurementTemplateSerializer(read_only=True)
    template_id = serializers.IntegerField(write_only=True, required=False)
    customer_name = serializers.CharField(
        source='customer.full_name',
        read_only=True
    )

    class Meta:
        model = CustomerMeasurement
        fields = (
            'id', 'customer', 'customer_name', 'template', 'template_id',
            'measurements', 'notes', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'customer', 'created_at', 'updated_at')


class CustomerMeasurementCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating customer measurements."""

    class Meta:
        model = CustomerMeasurement
        fields = ('template', 'measurements', 'notes')

    def validate_measurements(self, value):
        """Validate that measurements is a dictionary."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Measurements must be a dictionary.")
        return value

