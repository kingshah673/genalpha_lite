from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, ProductVariant, Category
from .cart import Cart

class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category', slug='test-cat')
        self.product = Product.objects.create(
            name='Test Product', 
            slug='test-product',
            category=self.category,
            base_price=100.00
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            size='M',
            color='Blue',
            stock_quantity=10
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
            'size': 'M',
            'color': 'Blue'
        })
        self.assertEqual(response.status_code, 200)
        
        # Verify session
        session = self.client.session
        cart = session.get('cart')
        self.assertTrue(cart)
        self.assertEqual(len(cart), 1)

    def test_cart_persistence(self):
        # Add item
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 2,
            'size': 'M',
            'color': 'Blue'
        })
        
        # Check if item persists in a new request (simulated by checking session)
        response = self.client.get(reverse('cart:detail'))
        self.assertContains(response, 'Test Product')
        self.assertContains(response, '200.0') # Total price

    def test_remove_from_cart(self):
        # Add item first
        self.client.post(reverse('cart:add'), {
            'product_id': self.product.id,
            'quantity': 1,
            'size': 'M',
            'color': 'Blue'
        })
        
        # Get variant ID since the cart uses it as key
        variant_id = str(self.variant.id)
        
        # Remove item
        response = self.client.post(reverse('cart:remove'), {
            'product_id': self.product.id,
            'variant_id': variant_id
        })
        self.assertEqual(response.status_code, 200)
        
        session = self.client.session
        cart = session.get('cart')
        self.assertEqual(len(cart), 0)
