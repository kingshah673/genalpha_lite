from django.db import models


class HeroBanner(models.Model):
    """Hero banner/slider model for homepage"""
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='banners/')
    link_url = models.CharField(max_length=500, blank=True, help_text="Optional link URL")
    button_text = models.CharField(max_length=50, blank=True, default="Shop Now")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
