import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Listar usuarios existentes
print("\n=== USUARIOS EXISTENTES ===")
for user in User.objects.all():
    print(f"Username: {user.username}, Email: {user.email}, Superusuario: {user.is_superuser}")

# Crear nuevo usuario de prueba
username = 'jhostin'
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, 'jhostin@example.com', '12345678')
    print(f"\n✅ Superusuario '{username}' creado exitosamente.")
    print(f"Username: {username}")
    print(f"Password: 12345678")
else:
    # Si existe, actualizar la contraseña
    user = User.objects.get(username=username)
    user.set_password('12345678')
    user.is_superuser = True
    user.is_staff = True
    user.role = 'ADMIN'
    user.save()
    print(f"\n✅ Contraseña del usuario '{username}' actualizada.")
    print(f"Username: {username}")
    print(f"Password: 12345678")
