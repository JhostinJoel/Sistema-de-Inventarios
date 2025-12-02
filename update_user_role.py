import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.users.models import User

# Update jhostin user to ADMIN role
try:
    user = User.objects.get(username='jhostin')
    user.role = 'ADMIN'
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print(f"✅ Usuario '{user.username}' actualizado:")
    print(f"   - Rol: {user.get_role_display()}")
    print(f"   - Superusuario: {user.is_superuser}")
    print(f"   - Staff: {user.is_staff}")
except User.DoesNotExist:
    print("❌ Usuario 'jhostin' no encontrado")

# Also update admin user if exists
try:
    admin_user = User.objects.get(username='admin')
    admin_user.role = 'ADMIN'
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print(f"\n✅ Usuario '{admin_user.username}' actualizado:")
    print(f"   - Rol: {admin_user.get_role_display()}")
    print(f"   - Superusuario: {admin_user.is_superuser}")
    print(f"   - Staff: {admin_user.is_staff}")
except User.DoesNotExist:
    print("\n❌ Usuario 'admin' no encontrado")

print("\n📋 Lista de todos los usuarios:")
for u in User.objects.all():
    print(f"   - {u.username}: {u.get_role_display()} (Superuser: {u.is_superuser})")
