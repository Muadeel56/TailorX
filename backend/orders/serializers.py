from rest_framework import serializers
from .models import Order, OrderItem
from users.serializers import UserSerializer
from measurements.serializers import CustomerMeasurementSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items."""

    class Meta:
        model = OrderItem
        fields = (
            'id', 'item_name', 'quantity', 'price',
            'measurements', 'special_instructions', 'created_at'
        )
        read_only_fields = ('id', 'created_at')


class OrderItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating order items."""

    class Meta:
        model = OrderItem
        fields = ('item_name', 'quantity', 'price', 'measurements', 'special_instructions')


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for orders with nested items."""
    customer = UserSerializer(read_only=True)
    tailor = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    customer_measurement = CustomerMeasurementSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    order_type_display = serializers.CharField(
        source='get_order_type_display',
        read_only=True
    )

    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'customer', 'tailor', 'order_type',
            'order_type_display', 'status', 'status_display',
            'total_price', 'deposit_amount', 'delivery_date',
            'customer_measurement', 'special_instructions',
            'items', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'order_number', 'created_at', 'updated_at')


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders."""
    items = OrderItemCreateSerializer(many=True)
    tailor_id = serializers.IntegerField()
    customer_measurement_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Order
        fields = (
            'tailor_id', 'order_type', 'total_price', 'deposit_amount',
            'delivery_date', 'customer_measurement_id', 'special_instructions', 'items'
        )

    def validate_tailor_id(self, value):
        """Validate that tailor exists and is a TAILOR user."""
        from users.models import User
        try:
            tailor = User.objects.get(id=value, user_type='TAILOR')
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid tailor ID or user is not a tailor.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        tailor_id = validated_data.pop('tailor_id')
        customer_measurement_id = validated_data.pop('customer_measurement_id', None)

        from users.models import User
        tailor = User.objects.get(id=tailor_id)
        customer = self.context['request'].user

        # Get customer measurement if provided
        customer_measurement = None
        if customer_measurement_id:
            from measurements.models import CustomerMeasurement
            try:
                customer_measurement = CustomerMeasurement.objects.get(
                    id=customer_measurement_id,
                    customer=customer
                )
            except CustomerMeasurement.DoesNotExist:
                pass

        # Create order
        order = Order.objects.create(
            customer=customer,
            tailor=tailor,
            customer_measurement=customer_measurement,
            **validated_data
        )

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating order status."""
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)

    def validate_status(self, value):
        """Validate status transition based on user role."""
        request = self.context.get('request')
        order = self.context.get('order')

        if not request or not order:
            return value

        user = request.user
        current_status = order.status

        # Customers can only cancel pending/confirmed orders
        if user.user_type == 'CUSTOMER':
            if value != 'CANCELLED':
                raise serializers.ValidationError(
                    "Customers can only cancel orders."
                )
            if current_status not in ['PENDING', 'CONFIRMED']:
                raise serializers.ValidationError(
                    f"Cannot cancel order with status: {current_status}"
                )

        # Tailors can update to IN_PROGRESS, READY, COMPLETED, or CANCELLED
        elif user.user_type == 'TAILOR':
            if value not in ['CONFIRMED', 'IN_PROGRESS', 'READY', 'COMPLETED', 'CANCELLED']:
                raise serializers.ValidationError(
                    "Invalid status transition for tailor."
                )
            # Validate status flow
            valid_transitions = {
                'PENDING': ['CONFIRMED', 'CANCELLED'],
                'CONFIRMED': ['IN_PROGRESS', 'CANCELLED'],
                'IN_PROGRESS': ['READY', 'CANCELLED'],
                'READY': ['COMPLETED'],
            }
            if current_status in valid_transitions:
                if value not in valid_transitions[current_status]:
                    raise serializers.ValidationError(
                        f"Cannot transition from {current_status} to {value}"
                    )

        return value

