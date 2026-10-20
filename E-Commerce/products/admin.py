from django.contrib import admin
from django.utils.html import format_html
from products.models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products Count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sku',
        'category',
        'price',
        'stock',
        'is_active',
        'stock_status',
        'thumbnail',
        'created_at',
    )
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'sku', 'description', 'category__name')
    list_editable = ('price', 'stock', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_per_page = 20

    def stock_status(self, obj):
        if obj.stock <= 0:
            return format_html('<span style="color:red; font-weight:bold;">Out of Stock</span>')
        elif obj.stock < 5:
            return format_html('<span style="color:orange; font-weight:bold;">Low Stock ({})</span>', obj.stock)
        return format_html('<span style="color:green;">In Stock ({})</span>', obj.stock)
    stock_status.short_description = 'Availability'

    def thumbnail(self, obj):
        return format_html(
            '<img src="{}" style="width: 45px; height: 35px; object-fit: cover; border-radius: 4px;" />',
            obj.image_url
        )
    thumbnail.short_description = 'Image'

    def image_preview(self, obj):
        return format_html(
            '<img src="{}" style="max-width: 250px; max-height: 200px; border-radius: 8px;" />',
            obj.image_url
        )
    image_preview.short_description = 'Image Preview'
