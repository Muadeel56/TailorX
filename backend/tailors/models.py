from django.db import models
from users.models import User


class TailorProfile(models.Model):
    """Tailor Profile model linked to User model for tailor-specific information."""
    
    SPECIALIZATION_CHOICES = [
        ('MENSWEAR', 'Menswear'),
        ('WOMENSWEAR', 'Womenswear'),
        ('KIDS', 'Kids'),
        ('FORMAL', 'Formal Wear'),
        ('CASUAL', 'Casual Wear'),
        ('CUSTOM', 'Custom Designs'),
    ]
    
    AVAILABILITY_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('BUSY', 'Busy'),
        ('UNAVAILABLE', 'Unavailable'),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tailor_profile'
    )
    shop_name = models.CharField(max_length=255)
    shop_address = models.TextField()
    specialization = models.CharField(
        max_length=20,
        choices=SPECIALIZATION_CHOICES
    )
    experience_years = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    total_reviews = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    portfolio_images = models.JSONField(default=list, blank=True)
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Tailor Profile'
        verbose_name_plural = 'Tailor Profiles'
    
    def save(self, *args, **kwargs):
        """Validate that user has user_type='TAILOR' before saving."""
        if self.user.user_type != 'TAILOR':
            raise ValueError("User must have user_type='TAILOR' to create a TailorProfile")
        super().save(*args, **kwargs)
    
    def __str__(self):
        """Return shop_name or user email for string representation."""
        return self.shop_name or self.user.email
