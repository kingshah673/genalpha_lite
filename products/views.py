from django.shortcuts import render, get_object_or_404
from .models import Product, Category, ProductVariant

def shop(request, category_slug=None):
    """Shop page view with filtering"""
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_active=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    # Sorting
    sort = request.GET.get('sort')
    if sort == 'price_asc':
        products = products.order_by('base_price')
    elif sort == 'price_desc':
        products = products.order_by('-base_price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
        
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'current_sort': sort,
    }
    return render(request, 'pages/shop.html', context)

def product_detail(request, slug):
    """Product detail view"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get available variants
    variants = product.variants.filter(is_available=True)
    sizes = variants.values_list('size', flat=True).distinct()
    colors = variants.values_list('color', flat=True).distinct()
    
    # Related products (same category, exclude current)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'variants': variants,
        'sizes': sizes,
        'colors': colors,
        'related_products': related_products,
    }
    return render(request, 'pages/product_detail.html', context)
