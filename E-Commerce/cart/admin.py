from django.contrib import admin
from cart.models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'item_price', 'subtotal_display')
    readonly_fields = ('item_price', 'subtotal_display')

    def item_price(self, obj):
        return f"₹{obj.product.price}" if obj.product else '-'
    item_price.short_description = 'Unit Price'

    def subtotal_display(self, obj):
        return f"₹{obj.subtotal:.2f}" if obj.pk else '-'
    subtotal_display.short_description = 'Subtotal'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart_items_count', 'cart_total', 'updated_at', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('cart_items_count', 'cart_total', 'created_at', 'updated_at')
    inlines = [CartItemInline]

    def cart_items_count(self, obj):
        return obj.total_items
    cart_items_count.short_description = 'Total Items'

    def cart_total(self, obj):
        return f"₹{obj.total_price:.2f}"
    cart_total.short_description = 'Cart Total'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'subtotal_display', 'created_at')
    search_fields = ('cart__user__username', 'product__name', 'product__sku')
    list_filter = ('created_at',)

    def subtotal_display(self, obj):
        return f"₹{obj.subtotal:.2f}"
    subtotal_display.short_description = 'Subtotal'
