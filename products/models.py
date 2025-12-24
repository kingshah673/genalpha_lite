from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator


class Category(models.Model):
    """Product category model"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def product_count(self):
        return self.products.filter(is_active=True).count()


class Product(models.Model):
    """Product model"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True, help_text="Is this product visible on the site?")
    is_featured = models.BooleanField(default=False, help_text="Show in Best Sellers section")
    is_new_arrival = models.BooleanField(default=False, help_text="Show in New Arrivals section")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def primary_image(self):
        """Get the primary product image"""
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()

    @property
    def price(self):
        """Return base price (can be extended for variants)"""
        return self.base_price

    @property
    def in_stock(self):
        """Check if any variant has stock"""
        return self.variants.filter(is_available=True, stock_quantity__gt=0).exists()

    @property
    def available_sizes(self):
        """Get list of available sizes"""
        return self.variants.filter(is_available=True, stock_quantity__gt=0).values_list('size', flat=True).distinct()

    @property
    def available_colors(self):
        """Get list of available colors"""
        return self.variants.filter(is_available=True, stock_quantity__gt=0).values_list('color', flat=True).distinct()


class ProductImage(models.Model):
    """Product image model - supports multiple images per product"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False, help_text="Main image for product card")
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', 'order']
        indexes = [
            models.Index(fields=['product', 'is_primary']),
        ]

    def __str__(self):
        return f"{self.product.name} - Image {self.order}"

    def save(self, *args, **kwargs):
        # Auto-set alt text if not provided
        if not self.alt_text:
            self.alt_text = f"{self.product.name} image"
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    """Product variant model for size/color combinations"""
    SIZE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double XL'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)
    color = models.CharField(max_length=50)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['product', 'size', 'color']
        ordering = ['size', 'color']
        indexes = [
            models.Index(fields=['product', 'is_available']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.size} / {self.color}"

    def save(self, *args, **kwargs):
        # Auto-generate SKU if not provided
        if not self.sku:
            base_sku = slugify(self.product.name)[:30]
            self.sku = f"{base_sku}-{self.size}-{slugify(self.color)}"
        super().save(*args, **kwargs)

    @property
    def in_stock(self):
        return self.is_available and self.stock_quantity > 0
