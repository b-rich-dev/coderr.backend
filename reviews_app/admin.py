from django.contrib import admin
from .models import Reviews


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Admin configuration for Reviews model"""
    
    list_display = ['id', 'business', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['business__user__username', 'reviewer__user__username', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_select_related = ['business__user', 'reviewer__user']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('business', 'reviewer', 'rating', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
