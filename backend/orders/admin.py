from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem model."""
    model = OrderItem
    extra = 1
    fields = ('item_name', 'quantity', 'price', 'measurements', 'special_instructions')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""
    
    inlines = [OrderItemInline]
    
    list_display = ('order_number', 'customer', 'tailor', 'order_type', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'order_type', 'created_at')
    search_fields = ('order_number', 'customer__email', 'customer__full_name', 'tailor__email', 'tailor__full_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'customer', 'tailor', 'order_type', 'status')
        }),
        ('Pricing', {
            'fields': ('total_price', 'deposit_amount')
        }),
        ('Delivery & Measurements', {
            'fields': ('delivery_date', 'customer_measurement')
        }),
        ('Additional Information', {
            'fields': ('special_instructions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
