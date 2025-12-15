import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

try:
    user = User.objects.get(username='admin')
    user.role = User.Role.ADMIN
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print("User 'admin' role updated to ADMIN.")
except User.DoesNotExist:
    print("User 'admin' not found.")
