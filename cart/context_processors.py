from .cart import Cart

def cart(request):
    """Context processor for cart data"""
    cart_obj = request.session.get('cart', {})
    cart_item_count = sum(item.get('quantity', 0) for item in cart_obj.values())
    
    return {
        'cart_item_count': cart_item_count
    }
