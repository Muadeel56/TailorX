from django.db import models
from users.models import User


class MeasurementTemplate(models.Model):
    """Measurement Template model for defining standard measurement templates."""
    
    MEASUREMENT_TYPE_CHOICES = [
        ('SHIRT', 'Shirt'),
        ('PANTS', 'Pants'),
        ('SUIT', 'Suit'),
        ('DRESS', 'Dress'),
        ('JACKET', 'Jacket'),
        ('CUSTOM', 'Custom'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    measurement_type = models.CharField(
        max_length=20,
        choices=MEASUREMENT_TYPE_CHOICES
    )
    standard_measurements = models.JSONField(
        default=dict,
        help_text="Standard measurement fields for this template"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Measurement Template'
        verbose_name_plural = 'Measurement Templates'
    
    def __str__(self):
        return self.name


class CustomerMeasurement(models.Model):
    """Customer Measurement model for storing customer-specific measurements."""
    
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='measurements'
    )
    template = models.ForeignKey(
        MeasurementTemplate,
        on_delete=models.CASCADE,
        related_name='customer_measurements'
    )
    measurements = models.JSONField(
        default=dict,
        help_text="Actual measurement values in key-value pairs"
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Customer Measurement'
        verbose_name_plural = 'Customer Measurements'
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        """Validate that customer has user_type='CUSTOMER' before saving."""
        if self.customer.user_type != 'CUSTOMER':
            raise ValueError("User must have user_type='CUSTOMER' to create a CustomerMeasurement")
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.customer.full_name} - {self.template.name}"
