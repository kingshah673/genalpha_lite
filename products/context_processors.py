from .models import Category

def categories_processor(request):
    """Add brands/categories to all templates for the navbar"""
    return {
        'all_categories': Category.objects.filter(is_active=True)
    }
