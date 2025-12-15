import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'video_user'
password = 'pass123'

if User.objects.filter(username=username).exists():
    User.objects.filter(username=username).delete()

User.objects.create_superuser(username, 'admin@example.com', password)
print(f"Superuser '{username}' created with password '{password}'.")
