from django.contrib import admin
from .models import TailorProfile


@admin.register(TailorProfile)
class TailorProfileAdmin(admin.ModelAdmin):
    """Admin configuration for TailorProfile model."""
    
    list_display = ('user', 'shop_name', 'specialization', 'availability_status', 'rating', 'total_reviews', 'created_at')
    list_filter = ('specialization', 'availability_status')
    search_fields = ('shop_name', 'user__email', 'user__full_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Shop Details', {
            'fields': ('shop_name', 'shop_address', 'specialization', 'bio')
        }),
        ('Experience & Ratings', {
            'fields': ('experience_years', 'rating', 'total_reviews')
        }),
        ('Availability', {
            'fields': ('availability_status',)
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Portfolio', {
            'fields': ('portfolio_images',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
