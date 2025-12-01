# Sistema de Inventario Inteligente 📦

Sistema completo de gestión de inventario desarrollado con Django, incluyendo punto de venta, control de stock, gestión de usuarios y chatbot con IA.

## 🚀 Características

- **Dashboard Interactivo**: Estadísticas en tiempo real de inventario y ventas
- **Gestión de Inventario**: CRUD completo para productos, categorías y almacenes
- **Punto de Venta (POS)**: Sistema de ventas con carrito dinámico
- **Gestión de Usuarios**: Sistema de autenticación con roles (Admin, Vendedor, Almacenista)
- **Auditoría**: Registro completo de todas las actividades del sistema
- **Chatbot IA**: Asistente inteligente powered by Google Gemini
- **Control de Stock**: Alertas de stock mínimo y movimientos de inventario

## 🛠️ Tecnologías

- **Backend**: Django 5.2.8
- **Base de Datos**: SQLite (desarrollo) / MySQL (producción)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **IA**: Google Gemini API
- **Containerización**: Docker

## 📋 Requisitos

- Python 3.14+
- Docker (opcional)
- Google Gemini API Key (para chatbot)

## 🔧 Instalación

### Opción 1: Instalación Local

```bash
# Clonar repositorio
git clone https://github.com/TU_USUARIO/inventory-system.git
cd inventory-system

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
# O usar el script:
python create_superuser.py

# Iniciar servidor
python manage.py runserver
```

### Opción 2: Docker

```bash
# Construir y ejecutar
docker-compose up --build

# Crear superusuario
docker-compose exec web python create_superuser.py
```

## ⚙️ Configuración

### Variables de Entorno (.env)

```env
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
GEMINI_API_KEY=tu-api-key-de-gemini

# Base de datos (opcional, por defecto usa SQLite)
DB_ENGINE=django.db.backends.mysql
DB_NAME=inventory_db
DB_USER=root
DB_PASSWORD=password
DB_HOST=db
DB_PORT=3306
```

### Obtener API Key de Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una API Key
3. Agrégala a tu archivo `.env`

## 📱 Uso

### Acceso al Sistema

- **URL**: http://localhost:8000
- **Panel Admin**: http://localhost:8000/admin
- **Usuario por defecto**: admin / admin

### Módulos Principales

1. **Dashboard** (`/`)
   - Vista general del sistema
   - Estadísticas de inventario
   - Actividad reciente

2. **Inventario** (`/inventory/`)
   - Productos (`/inventory/products/`)
   - Categorías (`/inventory/categories/`)
   - Almacenes (`/inventory/warehouses/`)

3. **Ventas** (`/sales/`)
   - Punto de Venta (`/sales/pos/`)
   - Historial de Ventas (`/sales/sales/`)
   - Clientes (`/sales/clients/`)

4. **Usuarios** (`/users/`)
   - Mi Perfil (`/users/profile/`)
   - Gestión de Usuarios (`/users/manage/`) - Solo Admin
   - Auditoría (`/users/audit-log/`) - Solo Admin

## 👥 Roles de Usuario

- **ADMIN**: Acceso completo al sistema
- **SELLER**: Acceso a ventas e inventario
- **WAREHOUSE**: Acceso a gestión de inventario

## 🗂️ Estructura del Proyecto

```
Proyecto1/
├── apps/
│   ├── chatbot/        # Módulo de chatbot IA
│   ├── dashboard/      # Dashboard principal
│   ├── inventory/      # Gestión de inventario
│   ├── notifications/  # Sistema de notificaciones
│   ├── sales/          # Módulo de ventas
│   └── users/          # Gestión de usuarios
├── config/             # Configuración de Django
├── static/             # Archivos estáticos
├── templates/          # Plantillas HTML
├── media/              # Archivos subidos
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── manage.py
```

## 📊 Base de Datos

**Ubicación**: `db.sqlite3`

**Herramientas recomendadas**:
- Django Admin Panel
- [DB Browser for SQLite](https://sqlitebrowser.org/)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

Tu Nombre - [GitHub](https://github.com/TU_USUARIO)

## 🙏 Agradecimientos

- Django Framework
- Google Gemini AI
- Bootstrap
- Font Awesome

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!
