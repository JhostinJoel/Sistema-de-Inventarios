import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.inventory.models import Category, Product

# Ensure Category exists
cat, created = Category.objects.get_or_create(name='General', defaults={'description': 'General Category'})
if created:
    print("Category 'General' created.")
else:
    print("Category 'General' exists.")

from apps.sales.models import Sale, SaleDetail
SaleDetail.objects.all().delete()
Sale.objects.all().delete()

# Clean up Demo Item if exists
Product.objects.filter(name='Demo Item').delete()
Product.objects.filter(name='Laptop Gamer').delete()
Product.objects.filter(name='Monitor 24"').delete()
print("Cleaned up products.")

from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='vendedor_demo').delete()
print("Cleaned up 'vendedor_demo' user.")
