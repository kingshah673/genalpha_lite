import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brandstore.settings")
django.setup()

from products.models import Product, Category

def check_missing():
    print("Checking for missing data...")
    
    # Check Products without images
    products_no_img = []
    for p in Product.objects.all():
        if not p.images.exists():
            products_no_img.append(p.name)
            
    if products_no_img:
        print(f"\nProducts with NO images ({len(products_no_img)}):")
        for name in products_no_img:
            print(f"- {name}")
    else:
        print("\nAll products have at least one image.")

    # Check empty categories
    print("\nCategory Counts:")
    for c in Category.objects.all():
        count = c.products.count()
        print(f"- {c.name}: {count} products")
        if count == 0:
            print(f"  WARNING: Category '{c.name}' is empty!")

if __name__ == "__main__":
    check_missing()
