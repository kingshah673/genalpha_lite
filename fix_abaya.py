import os
import sys
import django
import urllib.request
from django.core.files import File
from pathlib import Path

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brandstore.settings")
django.setup()

from products.models import Product, ProductImage
from django.conf import settings

# Alternative URL for the Abaya (or similar modest wear) that definitely works
ABAYA_IMG_URL = "https://images.pexels.com/photos/8112199/pexels-photo-8112199.jpeg?auto=compress&cs=tinysrgb&w=800"

def fix_abaya():
    try:
        product = Product.objects.get(name="Modest Abaya Set")
        print(f"Found product: {product.name}")
        
        if product.images.exists():
            print("Product already has images. Skipping.")
            return

        print("Downloading new image...")
        temp_path = Path(settings.MEDIA_ROOT) / 'temp_downloads'
        temp_path.mkdir(parents=True, exist_ok=True)
        img_filename = "abaya_fix.jpg"
        file_path = temp_path / img_filename
        
        req = urllib.request.Request(
            ABAYA_IMG_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
            out_file.write(response.read())
            
        with open(file_path, 'rb') as f:
            ProductImage.objects.create(
                product=product, 
                image=File(f, name=img_filename), 
                is_primary=True
            )
            
        os.remove(file_path)
        print("Success! Image added to Modest Abaya Set.")
        
    except Product.DoesNotExist:
        print("Product 'Modest Abaya Set' not found.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_abaya()
