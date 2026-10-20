from django.contrib import admin
from django.utils.html import format_html
from orders.models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'product_name', 'price', 'quantity', 'subtotal_display')
    readonly_fields = ('product', 'product_name', 'price', 'quantity', 'subtotal_display')

    def subtotal_display(self, obj):
        return f"₹{obj.subtotal:.2f}" if obj.pk else '-'
    subtotal_display.short_description = 'Subtotal'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'user',
        'full_name',
        'total_amount_display',
        'status_badge',
        'status',
        'payment_method',
        'created_at',
    )
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__username', 'full_name', 'email', 'phone_number')
    list_editable = ('status',)
    readonly_fields = ('order_number', 'user', 'total_amount_display', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
    list_per_page = 20

    def total_amount_display(self, obj):
        return f"₹{obj.total_amount:.2f}"
    total_amount_display.short_description = 'Total Amount'

    def status_badge(self, obj):
        colors = {
            Order.STATUS_PENDING: '#f39c12',
            Order.STATUS_CONFIRMED: '#2980b9',
            Order.STATUS_SHIPPED: '#8e44ad',
            Order.STATUS_DELIVERED: '#27ae60',
            Order.STATUS_CANCELLED: '#c0392b',
        }
        color = colors.get(obj.status, '#7f8c8d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 4px; font-weight: 500;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = 'Status Indicator'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'price', 'quantity', 'subtotal_display')
    search_fields = ('order__order_number', 'product_name')
    list_filter = ('order__created_at',)

    def subtotal_display(self, obj):
        return f"₹{obj.subtotal:.2f}"
    subtotal_display.short_description = 'Subtotal'
