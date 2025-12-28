from django.shortcuts import render
from .models import HeroBanner
from products.models import Category, Product

def home(request):
    """Homepage view"""
    # Get active hero banners
    banners = HeroBanner.objects.filter(is_active=True).order_by('order')
    
    # Get featured categories (top 3 for now, or add a featured flag to Category)
    categories = Category.objects.filter(is_active=True).order_by('order')[:3]
    
    # Get featured products (Best Sellers)
    featured_products = Product.objects.filter(
        is_active=True, 
        is_featured=True
    ).select_related('category').prefetch_related('images')[:4]
    
    # Get new arrivals
    new_arrivals = Product.objects.filter(
        is_active=True, 
        is_new_arrival=True
    ).select_related('category').prefetch_related('images')[:4]
    
    context = {
        'banners': banners,
        'categories': categories,
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'pages/home.html', context)

def robots_txt(request):
    scheme = request.scheme
    domain = request.get_host()
    return render(request, 'robots.txt', {'scheme': scheme, 'domain': domain}, content_type="text/plain")
