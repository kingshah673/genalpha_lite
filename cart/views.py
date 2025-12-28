from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import Product, ProductVariant
from .cart import Cart
from django.template.loader import render_to_string
from django.http import HttpResponse

@require_POST
def cart_add(request):
    """Add item to cart via HTMX"""
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')
    color = request.POST.get('color')
    
    product = get_object_or_404(Product, id=product_id)
    variant = None
    
    if size and color:
        variant = ProductVariant.objects.filter(product=product, size=size, color=color).first()
        if not variant:
            # If variant doesn't exist, return an error partial or just a message
            return HttpResponse("This combination is currently unavailable.", status=400)
    
    cart.add(product=product, quantity=quantity, variant=variant)
    
    # Return updated cart drawer content with trigger for navbar count
    response = render(request, 'components/cart_drawer_content.html', {'cart': cart})
    response['HX-Trigger'] = 'cartUpdated'
    return response

@require_POST
def cart_remove(request):
    """Remove item from cart via HTMX"""
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    variant_id = request.POST.get('variant_id')
    
    cart.remove(product_id=product_id, variant_id=variant_id)
    
    response = render(request, 'components/cart_drawer_content.html', {'cart': cart})
    response['HX-Trigger'] = 'cartUpdated'
    return response

@require_POST
def cart_update(request):
    """Update item quantity via HTMX"""
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    variant_id = request.POST.get('variant_id')
    quantity = int(request.POST.get('quantity', 1))
    
    product = get_object_or_404(Product, id=product_id)
    variant = None
    if variant_id and variant_id != 'None':
        variant = get_object_or_404(ProductVariant, id=variant_id)
        
    cart.add(product=product, quantity=quantity, variant=variant, update_quantity=True)
    
    response = render(request, 'components/cart_drawer_content.html', {'cart': cart})
    response['HX-Trigger'] = 'cartUpdated'
    return response

def cart_detail(request):
    """Full cart page"""
    cart = Cart(request)
    return render(request, 'pages/cart.html', {'cart': cart})

def cart_count(request):
    """Return just the cart count badge"""
    cart = Cart(request)
    return render(request, 'components/cart_count.html', {'cart_item_count': len(cart)})

def cart_drawer(request):
    """Return the cart drawer content partial"""
    cart = Cart(request)
    return render(request, 'components/cart_drawer_content.html', {'cart': cart})
