from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer
)


class OrderListView(generics.ListAPIView):
    """List orders filtered by user role."""

    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return orders based on user role."""
        user = self.request.user

        if user.user_type == 'CUSTOMER':
            return Order.objects.filter(customer=user).select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')
        elif user.user_type == 'TAILOR':
            return Order.objects.filter(tailor=user).select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')
        else:
            # Admin can see all orders
            return Order.objects.all().select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')


class OrderCreateView(generics.CreateAPIView):
    """Create a new order (customers only)."""

    serializer_class = OrderCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Ensure only customers can create orders."""
        if self.request.user.user_type != 'CUSTOMER':
            raise PermissionDenied("Only customers can create orders.")
        serializer.save()


class OrderDetailView(generics.RetrieveAPIView):
    """Get order details."""

    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        """Return orders user has access to."""
        user = self.request.user
        if user.user_type == 'CUSTOMER':
            return Order.objects.filter(customer=user).select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')
        elif user.user_type == 'TAILOR':
            return Order.objects.filter(tailor=user).select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')
        else:
            return Order.objects.all().select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')

    def get_object(self):
        """Ensure user can only access their own orders."""
        obj = super().get_object()
        user = self.request.user
        if user.user_type not in ['ADMIN'] and obj.customer != user and obj.tailor != user:
            raise PermissionDenied("You do not have permission to access this order.")
        return obj


class OrderStatusUpdateView(generics.UpdateAPIView):
    """Update order status."""

    serializer_class = OrderStatusUpdateSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        """Return orders user can update."""
        user = self.request.user
        if user.user_type == 'TAILOR':
            return Order.objects.filter(tailor=user).select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')
        elif user.user_type == 'CUSTOMER':
            return Order.objects.filter(customer=user).select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')
        else:
            return Order.objects.all().select_related(
                'customer', 'tailor', 'customer_measurement'
            ).prefetch_related('items')

    def get_object(self):
        """Get order and validate access."""
        obj = super().get_object()
        user = self.request.user

        # Ensure user is either customer or tailor
        if obj.customer != user and obj.tailor != user and user.user_type != 'ADMIN':
            raise PermissionDenied("You do not have permission to update this order.")

        return obj

    def update(self, request, *args, **kwargs):
        """Update order status with validation."""
        order = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            context={'request': request, 'order': order}
        )
        serializer.is_valid(raise_exception=True)

        order.status = serializer.validated_data['status']
        order.save()

        return Response(OrderSerializer(order).data)


class OrderCancelView(generics.DestroyAPIView):
    """Cancel an order (customers only, if status allows)."""

    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        """Return customer's orders."""
        return Order.objects.filter(customer=self.request.user).select_related(
            'customer', 'tailor', 'customer_measurement'
        ).prefetch_related('items')

    def destroy(self, request, *args, **kwargs):
        """Cancel order by updating status instead of deleting."""
        order = self.get_object()

        if order.status not in ['PENDING', 'CONFIRMED']:
            return Response(
                {"error": f"Cannot cancel order with status: {order.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = 'CANCELLED'
        order.save()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_200_OK
        )
