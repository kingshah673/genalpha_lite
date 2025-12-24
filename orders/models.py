from django.db import models
from django.core.validators import MinValueValidator
from products.models import Product, ProductVariant
import uuid


class Order(models.Model):
    """Order model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        # Future: stripe, paypal, etc.
    ]

    order_number = models.CharField(max_length=50, unique=True, blank=True, editable=False)
    
    # Customer information
    customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20, blank=True)
    
    # Order details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='cash_on_delivery')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Admin notes
    notes = models.TextField(blank=True, help_text="Internal notes for admin")

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['order_number']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_order_number():
        """Generate unique order number with format: ORD-YYYYMMDD-XXXX"""
        from datetime import datetime
        date_str = datetime.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4().hex)[:6].upper()
        return f"ORD-{date_str}-{unique_id}"

    @property
    def item_count(self):
        """Total number of items in the order"""
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    """Order item model - individual products in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, null=True, blank=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], 
                                 help_text="Price at time of purchase")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        indexes = [
            models.Index(fields=['order']),
        ]

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # Auto-calculate subtotal
        self.subtotal = self.price * self.quantity
        super().save(*args, **kwargs)

    @property
    def variant_details(self):
        """Get variant size and color for display"""
        if self.variant:
            return f"{self.variant.size} / {self.variant.color}"
        return "N/A"
