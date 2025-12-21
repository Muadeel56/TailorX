from django.db import models
from django.utils import timezone
from users.models import User
from measurements.models import CustomerMeasurement
import uuid


class Order(models.Model):
    """Order model for managing customer orders with tailors."""
    
    ORDER_TYPE_CHOICES = [
        ('SHIRT', 'Shirt'),
        ('PANTS', 'Pants'),
        ('SUIT', 'Suit'),
        ('DRESS', 'Dress'),
        ('JACKET', 'Jacket'),
        ('CUSTOM', 'Custom'),
        ('MULTIPLE', 'Multiple Items'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('IN_PROGRESS', 'In Progress'),
        ('READY', 'Ready for Pickup'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_orders'
    )
    tailor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tailor_orders'
    )
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_date = models.DateField(null=True, blank=True)
    customer_measurement = models.ForeignKey(
        CustomerMeasurement,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """Generate unique order_number if not set and validate user types."""
        if not self.order_number:
            date_str = timezone.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8].upper()
            self.order_number = f"ORD-{date_str}-{unique_id}"
        
        # Validation
        if self.customer.user_type != 'CUSTOMER':
            raise ValueError("Customer must have user_type='CUSTOMER'")
        if self.tailor.user_type != 'TAILOR':
            raise ValueError("Tailor must have user_type='TAILOR'")
        
        super().save(*args, **kwargs)
    
    def calculate_total(self):
        """Calculate total price from order items."""
        return sum(item.price * item.quantity for item in self.items.all())
    
    def __str__(self):
        return f"{self.order_number} - {self.customer.full_name}"


class OrderItem(models.Model):
    """OrderItem model for storing individual items within an order."""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    measurements = models.JSONField(
        default=dict,
        help_text="Item-specific measurements"
    )
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
    
    def __str__(self):
        return f"{self.order.order_number} - {self.item_name} (x{self.quantity})"
