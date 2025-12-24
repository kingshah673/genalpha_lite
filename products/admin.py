from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from .models import Category, Product, ProductImage, ProductVariant


class ProductImageInline(admin.TabularInline):
    """Inline for managing product images"""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


class ProductVariantInline(admin.TabularInline):
    """Inline for managing product variants"""
    model = ProductVariant
    extra = 1
    fields = ('size', 'color', 'sku', 'stock_quantity', 'is_available')


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Admin for Category model with sortable feature"""
    list_display = ('name', 'slug', 'image_preview', 'product_count', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview', 'product_count')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Image'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model"""
    list_display = ('name', 'category', 'base_price', 'stock_status', 'is_featured', 
                    'is_new_arrival', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'is_new_arrival', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'is_featured', 'is_new_arrival')
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ('created_at', 'updated_at', 'stock_status')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('base_price',)
        }),
        ('Product Flags', {
            'fields': ('is_active', 'is_featured', 'is_new_arrival')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'stock_status'),
            'classes': ('collapse',)
        }),
    )

    actions = ['make_active', 'make_inactive', 'mark_as_featured', 'unmark_as_featured']

    def stock_status(self, obj):
        if obj.in_stock:
            return format_html('<span style="color: green;">✓ In Stock</span>')
        return format_html('<span style="color: red;">✗ Out of Stock</span>')
    stock_status.short_description = 'Stock'

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Activate selected products"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Deactivate selected products"

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark as featured"

    def unmark_as_featured(self, request, queryset):
        queryset.update(is_featured=False)
    unmark_as_featured.short_description = "Remove from featured"


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin for ProductImage model"""
    list_display = ('product', 'image_preview', 'alt_text', 'is_primary', 'order')
    list_filter = ('is_primary', 'product')
    search_fields = ('product__name', 'alt_text')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Admin for ProductVariant model"""
    list_display = ('product', 'size', 'color', 'sku', 'stock_quantity', 'is_available')
    list_filter = ('size', 'is_available', 'product__category')
    search_fields = ('product__name', 'sku', 'color')
    list_editable = ('stock_quantity', 'is_available')
