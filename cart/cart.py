from decimal import Decimal
from django.conf import settings
from products.models import Product, ProductVariant

class Cart:
    def __init__(self, request):
        """Initialize the cart"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, variant=None, update_quantity=False):
        """Add a product to the cart or update its quantity"""
        product_id = str(product.id)
        
        # Create a unique key for the item (Product ID + Variant ID)
        item_key = product_id
        if variant:
            item_key = f"{product_id}_{variant.id}"
            
        if item_key not in self.cart:
            self.cart[item_key] = {
                'quantity': 0,
                'price': str(product.base_price),
                'product_id': product.id,
                'variant_id': variant.id if variant else None,
            }
            
        if update_quantity:
            self.cart[item_key]['quantity'] = quantity
        else:
            self.cart[item_key]['quantity'] += quantity
            
        self.save()

    def save(self):
        """Mark the session as modified to ensure it gets saved"""
        self.session.modified = True

    def remove(self, product_id, variant_id=None):
        """Remove a product from the cart"""
        item_key = str(product_id)
        if variant_id:
            item_key = f"{product_id}_{variant_id}"
            
        if item_key in self.cart:
            del self.cart[item_key]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the products from the database"""
        cart = self.cart.copy()
        
        # We need to fetch products and variants to display them
        # Group by product IDs to minimize queries, though loop is simpler for now
        # Ideally we'd optimize this, but for session cart it's okay.
        
        for item_key, item in cart.items():
            item = item.copy()
            product_id = item['product_id']
            variant_id = item.get('variant_id')
            
            # Fetch product (could be optimized)
            try:
                product = Product.objects.get(id=product_id)
                item['product'] = product
            except Product.DoesNotExist:
                continue
                
            if variant_id:
                try:
                    variant = ProductVariant.objects.get(id=variant_id)
                    item['variant'] = variant
                except ProductVariant.DoesNotExist:
                    item['variant'] = None
            else:
                item['variant'] = None
                
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            
            yield item

    def __len__(self):
        """Count all items in the cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate total cost"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Remove cart from session"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
