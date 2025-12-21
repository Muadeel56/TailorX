from django.contrib import admin
from .models import MeasurementTemplate, CustomerMeasurement


@admin.register(MeasurementTemplate)
class MeasurementTemplateAdmin(admin.ModelAdmin):
    """Admin configuration for MeasurementTemplate model."""
    
    list_display = ('name', 'measurement_type', 'created_at')
    list_filter = ('measurement_type', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('name', 'description', 'measurement_type')}),
        ('Standard Measurements', {'fields': ('standard_measurements',)}),
        ('Important Dates', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(CustomerMeasurement)
class CustomerMeasurementAdmin(admin.ModelAdmin):
    """Admin configuration for CustomerMeasurement model."""
    
    list_display = ('customer', 'template', 'created_at')
    list_filter = ('template', 'created_at')
    search_fields = ('customer__email', 'customer__full_name', 'template__name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('customer', 'template')
    
    fieldsets = (
        (None, {'fields': ('customer', 'template')}),
        ('Measurements', {'fields': ('measurements', 'notes')}),
        ('Important Dates', {'fields': ('created_at', 'updated_at')}),
    )
