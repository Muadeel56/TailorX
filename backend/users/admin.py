from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin configuration for User model."""
    
    list_display = ('email', 'full_name', 'user_type', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('email', 'full_name', 'phone')
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone', 'address', 'profile_picture')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff')}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
    )
