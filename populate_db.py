import os
import django
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sneakers_ecommerce.settings')
django.setup()

from shop.models import Category, Product

def populate():
    # 1. Create Categories
    categories_data = [
        {'name': 'Running', 'slug': 'running', 'description': 'Zapatillas para correr y entrenamiento de alto rendimiento.'},
        {'name': 'Casual', 'slug': 'casual', 'description': 'Estilo diario y comodidad para la ciudad.'},
        {'name': 'Basketball', 'slug': 'basketball', 'description': 'Máximo soporte y tracción en la cancha.'},
        {'name': 'Skateboarding', 'slug': 'skateboarding', 'description': 'Durabilidad y estilo urbano para la tabla.'},
    ]

    categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={'name': cat_data['name'], 'description': cat_data['description']}
        )
        categories[cat_data['slug']] = cat
        if created:
            print(f"Categoría creada: {cat.name}")

    # 2. Create Products
    products_data = [
        # Running
        {
            'name': 'Nike Air Zoom Pegasus 40',
            'slug': 'nike-pegasus-40',
            'category': categories['running'],
            'brand': 'Nike',
            'price': 129.99,
            'description': 'La Pegasus 40 regresa con su sensación elástica característica para ayudarte a alcanzar tus objetivos de running.',
            'color': 'Blanco/Azul',
            'sizes': '38,39,40,41,42,43,44,45',
            'stock': 15,
            'featured': True
        },
        {
            'name': 'Adidas Ultraboost Light',
            'slug': 'adidas-ultraboost-light',
            'category': categories['running'],
            'brand': 'Adidas',
            'price': 189.99,
            'description': 'Experimenta una energía épica con los nuevos Ultraboost Light, nuestros Ultraboost más ligeros.',
            'color': 'Negro/Solar Red',
            'sizes': '39,40,41,42,43,44',
            'stock': 10,
            'featured': True
        },
        # Casual
        {
            'name': 'Nike Air Force 1 07',
            'slug': 'nike-air-force-1',
            'category': categories['casual'],
            'brand': 'Nike',
            'price': 110.00,
            'description': 'El resplandor sigue vivo en las Nike Air Force 1 07, el modelo original de baloncesto que da un giro innovador.',
            'color': 'Blanco',
            'sizes': '36,37,38,39,40,41,42,43,44,45',
            'stock': 25,
            'featured': True
        },
        {
            'name': 'Adidas Forum Low',
            'slug': 'adidas-forum-low',
            'category': categories['casual'],
            'brand': 'Adidas',
            'price': 100.00,
            'description': 'Más que una zapatilla, es una declaración de intenciones. Las adidas Forum aparecieron en el 84.',
            'color': 'Azul/Blanco',
            'sizes': '40,41,42,43,44',
            'stock': 12,
            'featured': False
        },
        {
            'name': 'New Balance 550',
            'slug': 'nb-550-white',
            'category': categories['casual'],
            'brand': 'New Balance',
            'price': 120.00,
            'description': 'El regreso de una leyenda. La 550 original de 1989 dejó su huella en las canchas de baloncesto de costa a costa.',
            'color': 'Blanco/Gris',
            'sizes': '38,39,40,41,42,43,44',
            'stock': 8,
            'featured': True
        },
        # Basketball
        {
            'name': 'Jordan Air Jordan 1 Retro High',
            'slug': 'jordan-1-retro',
            'category': categories['basketball'],
            'brand': 'Jordan',
            'price': 180.00,
            'description': 'Familiar pero siempre innovadora, la Air Jordan 1 se actualiza para la cultura actual de los amantes de las zapatillas.',
            'color': 'Rojo/Negro/Blanco',
            'sizes': '40,41,42,43,44,45,46',
            'stock': 5,
            'featured': True
        },
        {
            'name': 'LeBron 21 Tahitian',
            'slug': 'lebron-21-tahitian',
            'category': categories['basketball'],
            'brand': 'Nike',
            'price': 200.00,
            'description': 'Las LeBron 21 cuentan con un sistema de cables que funciona con la amortiguación Zoom Air.',
            'color': 'Negro/Verde',
            'sizes': '41,42,43,44,45',
            'stock': 7,
            'featured': False
        }
    ]

    for prod_data in products_data:
        prod, created = Product.objects.get_or_create(
            slug=prod_data['slug'],
            defaults=prod_data
        )
        if created:
            print(f"Producto creado: {prod.name}")
        else:
            # Update existing to ensure stock/prices are set
            for key, value in prod_data.items():
                setattr(prod, key, value)
            prod.save()
            print(f"Producto actualizado: {prod.name}")

    print("¡Población de datos completada!")

if __name__ == '__main__':
    populate()
