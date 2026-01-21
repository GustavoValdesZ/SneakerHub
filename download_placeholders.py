import os
import django
import requests
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sneakers_ecommerce.settings')
django.setup()

from shop.models import Product

def download_placeholders():
    # Primary: #00ffff (Cyan), Background: #0a0a23 (Midnight Navy)
    # Secondary: #ff003c (Solar Red)
    bg_color = "0a0a23"
    text_color = "00ffff"
    
    products_to_update = [
        ('Converse Chuck Taylor All Star Hi', 'converse-chuck-hi'),
        ('Vans Old Skool', 'vans-old-skool'),
        ('Adidas Samba OG', 'adidas-samba-og'),
        ('Nike Dunk Low Panda', 'nike-dunk-panda'),
        ('LeBron 21 Tahitian', 'lebron-21-tahitian'),
        ('Adidas Forum Low', 'adidas-forum-low'),
    ]

    for name, slug in products_to_update:
        try:
            product = Product.objects.get(slug=slug)
            
            # Create placeholder URL
            # Format: https://placehold.co/800x800/bg/text.png?text=Product+Name
            safe_text = name.replace(' ', '+')
            url = f"https://placehold.co/800x800/{bg_color}/{text_color}.png?text={safe_text}"
            
            print(f"Downloading placeholder for: {name}...")
            response = requests.get(url)
            
            if response.status_code == 200:
                filename = f"{slug}.png"
                product.image.save(filename, ContentFile(response.content), save=True)
                print(f"Successfully updated image for: {name}")
            else:
                print(f"Failed to download image for {name}: {response.status_code}")
                
        except Product.DoesNotExist:
            print(f"Product not found: {slug}")
        except Exception as e:
            print(f"Error processing {name}: {str(e)}")

if __name__ == '__main__':
    download_placeholders()
