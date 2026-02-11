from django.contrib import admin
from .models import Orders


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    """Admin configuration for Orders model"""
    
    list_display = ['id', 'title', 'customer', 'business', 'status', 'price', 'created_at']
    list_filter = ['status', 'offer_type', 'created_at']
    search_fields = ['title', 'customer__user__username', 'business__user__username']
    readonly_fields = ['created_at', 'updated_at', 'offer_detail']
    list_select_related = ['customer__user', 'business__user', 'offer_detail']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('offer_detail', 'customer', 'business', 'status')
        }),
        ('Offer Details Snapshot', {
            'fields': ('title', 'offer_type', 'price', 'delivery_time_in_days', 'revisions', 'features')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        """Make snapshot fields readonly after creation"""
        
        if obj:
            return self.readonly_fields + ('title', 'offer_type', 'price', 'delivery_time_in_days', 'revisions', 'features', 'customer', 'business')
        return self.readonly_fields
