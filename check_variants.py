from products.models import Product, ProductVariant
try:
    p = Product.objects.get(id=1)
    print(f'Product: {p.name}')
    variants = ProductVariant.objects.filter(product=p)
    print(f'Variants count: {variants.count()}')
    for v in variants:
        print(f' - {v.color}, {v.size}, Qty: {v.stock_quantity}')
except Exception as e:
    print(f'Error: {e}')
