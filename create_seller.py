import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

if not User.objects.filter(username='Greisy123').exists():
    user = User.objects.create_user('Greisy123', 'greisy@example.com', 'user')
    user.role = User.Role.SELLER
    user.save()
    print("Seller 'Greisy123' created.")
else:
    print("Seller 'Greisy123' already exists.")
