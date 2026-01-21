import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sneakers_ecommerce.settings')
django.setup()

from shop.models import Product, Category

def expand_catalog():
    # Update NB 550 to the new pristine image
    try:
        nb550 = Product.objects.get(slug='nb-550-white')
        nb550.image = 'products/nb-550-white.png'
        nb550.save()
        print("Updated New Balance 550 to pristine image.")
    except Product.DoesNotExist:
        print("NB 550 not found.")

    # Categories
    cat_running = Category.objects.get(slug='running')
    cat_casual = Category.objects.get(slug='casual')
    cat_basketball = Category.objects.get(slug='basketball')
    cat_skate = Category.objects.get(slug='skateboarding')

    # New Products to add
    new_products = [
        {
            'name': 'Nike Dunk Low Panda',
            'category': cat_casual,
            'description': 'The iconic black and white colorway that goes with everything. A must-have for any collection.',
            'price': 110.00,
            'stock': 25,
            'slug': 'nike-dunk-panda'
        },
        {
            'name': 'Adidas Samba OG',
            'category': cat_casual,
            'description': 'The terrace classic. Black leather with white stripes and a gum sole.',
            'price': 100.00,
            'stock': 30,
            'slug': 'adidas-samba-og'
        },
        {
            'name': 'Vans Old Skool',
            'category': cat_skate,
            'description': 'The classic skate shoe. Durable canvas and suede upper with the signature side stripe.',
            'price': 70.00,
            'stock': 40,
            'slug': 'vans-old-skool'
        },
        {
            'name': 'Converse Chuck Taylor All Star Hi',
            'category': cat_casual,
            'description': 'The most iconic sneaker in the world. High-top canvas classic.',
            'price': 65.00,
            'stock': 50,
            'slug': 'converse-chuck-hi'
        }
    ]

    for p_data in new_products:
        product, created = Product.objects.get_or_create(
            slug=p_data['slug'],
            defaults={
                'name': p_data['name'],
                'category': p_data['category'],
                'description': p_data['description'],
                'price': p_data['price'],
                'stock': p_data['stock'],
            }
        )
        if created:
            print(f"Created new product: {product.name}")
        else:
            print(f"Product already exists: {product.name}")

if __name__ == '__main__':
    expand_catalog()
