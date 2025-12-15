import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.inventory.models import Product

print("Checking products and images...")
for p in Product.objects.all():
    print(f"Product: {p.name}, Image: {p.image}, Image URL: {p.image.url if p.image else 'None'}")
