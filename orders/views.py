from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.cart import Cart
from products.models import ProductVariant

def checkout(request):
    """Checkout view"""
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('cart:detail')
        
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items
            for item in cart:
                product = item['product']
                variant_id = item.get('variant_id')
                variant = None
                
                # Check for variant
                if variant_id:
                    try:
                        variant = ProductVariant.objects.get(id=variant_id)
                        # Basic stock check/update could go here, but omitted for MVP simplicity
                        # In production we should lock rows or check stock again
                        variant.stock_quantity -= item['quantity']
                        variant.save()
                    except ProductVariant.DoesNotExist:
                        pass
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    variant=variant,
                    quantity=item['quantity'],
                    price=item['price'],
                    subtotal=item['total_price']
                )
            
            # Clear cart
            cart.clear()
            
            return redirect('orders:confirmation', order_number=order.order_number)
    else:
        form = CheckoutForm()
        
    context = {
        'cart': cart,
        'form': form,
    }
    return render(request, 'pages/checkout.html', context)

def order_confirmation(request, order_number):
    """Order confirmation view"""
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'pages/order_confirmation.html', {'order': order})
