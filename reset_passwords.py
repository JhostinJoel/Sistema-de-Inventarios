import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

def reset_password(username, new_password):
    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        print(f"✅ Password for user '{username}' updated successfully.")
    except User.DoesNotExist:
        print(f"❌ User '{username}' not found.")

# Admins -> password: 'admin'
reset_password('admin', 'admin')
reset_password('jhostin', 'admin')

# Sellers -> password: 'user'
reset_password('Greisy123', 'user')
