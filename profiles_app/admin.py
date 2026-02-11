from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin configuration for Profile model"""
    
    list_display = ['id', 'user', 'type', 'location', 'tel', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['user__username', 'user__email', 'location', 'description']
    readonly_fields = ['created_at']
    list_select_related = ['user']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'type')
        }),
        ('Profile Details', {
            'fields': ('file', 'location', 'tel', 'description', 'working_hours')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
