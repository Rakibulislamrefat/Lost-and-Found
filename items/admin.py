from django.contrib import admin
from .models import Item, ClaimRequest


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'category', 'status', 'user', 'location', 'date_reported', 'created_at')
    list_filter = ('item_type', 'category', 'status', 'date_reported')
    search_fields = ('title', 'description', 'location')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ClaimRequest)
class ClaimRequestAdmin(admin.ModelAdmin):
    list_display = ('item', 'claimant', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('item__title', 'claimant__username', 'message')
    list_editable = ('status',)
