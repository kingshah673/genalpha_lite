from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminMixin
from .models import HeroBanner


@admin.register(HeroBanner)
class HeroBannerAdmin(SortableAdminMixin, admin.ModelAdmin):
    """Admin for HeroBanner model"""
    list_display = ('title', 'image_preview', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px;" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'
