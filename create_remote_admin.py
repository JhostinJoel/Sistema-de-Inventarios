import os
import django

# Configure the remote database URL directly
os.environ['DATABASE_URL'] = 'postgresql://inventario_db_0xpo_user:1FUPJbHK6bZZtOsjoIcWsDZYyNYeeDWK@dpg-d4ni9bngi27c73fg4f50-a.oregon-postgres.render.com/inventario_db_0xpo'

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

def create_remote_admin():
    User = get_user_model()
    username = 'admin_render'
    email = 'admin@example.com'
    password = 'password123'

    print("Conectando a la base de datos de Render...")
    
    try:
        if not User.objects.filter(username=username).exists():
            print(f"Creando superusuario '{username}'...")
            user = User.objects.create_superuser(username, email, password)
            # IMPORTANT: Set the role to ADMIN explicitly
            user.role = 'ADMIN'
            user.save()
            print(f"\n✅ ¡ÉXITO! Usuario creado en la nube.")
            print(f"Usuario: {username}")
            print(f"Contraseña: {password}")
            print(f"Rol: {user.role}")
        else:
            print(f"\n⚠️ El usuario '{username}' ya existe.")
            u = User.objects.get(username=username)
            u.set_password(password)
            # FIX: Ensure role is ADMIN
            u.role = 'ADMIN'
            u.is_superuser = True
            u.is_staff = True
            u.save()
            print(f"✅ Contraseña actualizada y ROL fijado a ADMIN.")
            print(f"Usuario: {username}")
            print(f"Rol actual: {u.role}")
            
    except Exception as e:
        print(f"\n❌ Error conectando a la base de datos: {e}")

if __name__ == '__main__':
    create_remote_admin()
