from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category, ProductVariant
from django.db.models import Q

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
    
    # Get available variants and valid combinations
    variants = product.variants.filter(is_available=True, stock_quantity__gt=0)
    sizes = variants.values_list('size', flat=True).distinct()
    colors = variants.values_list('color', flat=True).distinct()
    
    # Create a list of valid color/size combinations for Alpine.js
    valid_combinations = list(variants.values('color', 'size'))
    
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
        'valid_combinations': valid_combinations,
        'related_products': related_products,
    }
    return render(request, 'pages/product_detail.html', context)

def search(request):
    """Full search results view"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    
    context = {
        'products': products,
        'query': query,
        'categories': Category.objects.filter(is_active=True),
    }
    return render(request, 'pages/shop.html', context)

def search_suggestions(request):
    """Real-time search suggestions view (HTMX)"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return HttpResponse('')
        
    products = Product.objects.filter(
        is_active=True
    ).filter(
        Q(name__icontains=query) | 
        Q(category__name__icontains=query)
    ).distinct()[:5]
    
    return render(request, 'components/search_suggestions.html', {'products': products})
