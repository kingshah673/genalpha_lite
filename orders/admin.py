from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline for order items - read only"""
    model = OrderItem
    extra = 0
    can_delete = False
    fields = ('product', 'variant_info', 'quantity', 'price', 'subtotal')
    readonly_fields = ('product', 'variant_info', 'quantity', 'price', 'subtotal')

    def variant_info(self, obj):
        return obj.variant_details if obj.variant else "N/A"
    variant_info.short_description = 'Size / Color'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin for Order model"""
    list_display = ('order_number', 'customer_name', 'phone', 'city', 'total_amount', 
                    'status_badge', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at', 'city')
    search_fields = ('order_number', 'customer_name', 'phone', 'email')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'item_count')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'status', 'payment_method', 'item_count')
        }),
        ('Customer Information', {
            'fields': ('customer_name', 'phone', 'email', 'address', 'city', 'postal_code')
        }),
        ('Payment', {
            'fields': ('total_amount',)
        }),
        ('Admin Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of orders
        return False

    # Allow status updates
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing order
            return ('order_number', 'customer_name', 'phone', 'email', 'address', 
                    'city', 'postal_code', 'total_amount', 'payment_method', 
                    'created_at', 'updated_at', 'item_count')
        return ('order_number', 'created_at', 'updated_at', 'item_count')
