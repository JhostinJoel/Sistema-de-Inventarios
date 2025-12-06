import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

users = User.objects.all()

print(f"{'USERNAME':<20} | {'ROLE':<15} | {'EMAIL':<30} | {'IS_ACTIVE':<10}")
print("-" * 85)

for user in users:
    print(f"{user.username:<20} | {user.role:<15} | {user.email:<30} | {str(user.is_active):<10}")
