from django.contrib import admin
from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    """Inline admin for OfferDetail within Offer admin"""
    
    model = OfferDetail
    extra = 0
    fields = ['title', 'offer_type', 'price', 'delivery_time_in_days', 'revisions', 'features']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    """Admin configuration for Offer model"""
    
    list_display = ['id', 'title', 'creator', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'description', 'creator__user__username']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OfferDetailInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('creator', 'title', 'description', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    """Admin configuration for OfferDetail model"""
    
    list_display = ['id', 'offer', 'title', 'offer_type', 'price', 'delivery_time_in_days', 'revisions']
    list_filter = ['offer_type']
    search_fields = ['title', 'offer__title']
    list_select_related = ['offer']
