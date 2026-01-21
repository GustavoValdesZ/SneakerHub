import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sneakers_ecommerce.settings')
django.setup()

from shop.models import Product

def update_images():
    image_map = {
        'nike-pegasus-40': 'products/nike-pegasus-40.png',
        'adidas-ultraboost-light': 'products/adidas-ultraboost-light.png',
        'nike-air-force-1': 'products/nike-air-force-1.png',
        'jordan-1-retro': 'products/jordan-1-retro.png',
        'nb-550-white': 'products/nb-550-white.png',
    }

    for slug, image_path in image_map.items():
        try:
            product = Product.objects.get(slug=slug)
            product.image = image_path
            product.save()
            print(f"Imagen actualizada para: {product.name}")
        except Product.DoesNotExist:
            print(f"Producto no encontrado: {slug}")

if __name__ == '__main__':
    update_images()
