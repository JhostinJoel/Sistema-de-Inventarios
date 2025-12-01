# Instrucciones de Restauración de Base de Datos

Este archivo contiene instrucciones para usar los exports de la base de datos.

## Archivos Disponibles

1. **db_export.json** - Export completo en formato JSON (Django fixtures)
2. **db_backup.sqlite3** - Copia binaria de la base de datos SQLite

## Opción 1: Usar el Export JSON (Recomendado)

### Ventajas:
- Portable entre diferentes bases de datos (SQLite, MySQL, PostgreSQL)
- Legible y editable
- Compatible con el sistema de fixtures de Django

### Restaurar:

```bash
# 1. Aplicar migraciones
python manage.py migrate

# 2. Cargar datos
python manage.py loaddata db_export.json
```

## Opción 2: Copiar la Base de Datos SQLite Directamente

### Ventajas:
- Más rápido
- Incluye todo (incluso datos no exportables)

### Restaurar:

```bash
# 1. Asegúrate de que NO existe db.sqlite3
# 2. Copia el backup
copy db_backup.sqlite3 db.sqlite3

# En Linux/Mac:
cp db_backup.sqlite3 db.sqlite3
```

## Usuarios Incluidos en la Base de Datos

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| admin | password123 | Administrador |

> ⚠️ **IMPORTANTE**: Cambia las contraseñas en producción

## Datos Incluidos

La base de datos exportada contiene:
- ✅ Usuarios y permisos
- ✅ Categorías de productos
- ✅ Almacenes
- ✅ Productos de ejemplo
- ✅ Clientes
- ✅ Proveedores
- ✅ Ventas de ejemplo
- ✅ Configuraciones del sistema

## Crear tu Propia Base de Datos

Si prefieres empezar desde cero:

```bash
# 1. Elimina la base de datos actual (si existe)
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows

# 2. Ejecuta migraciones
python manage.py migrate

# 3. Crea superusuario
python manage.py createsuperuser

# 4. (Opcional) Carga datos de ejemplo
python manage.py loaddata initial_data.json
```

## Troubleshooting

### Error: "Duplicate entry"
```bash
# Limpia la base de datos y vuelve a empezar
python manage.py flush
python manage.py loaddata db_export.json
```

### Error: "Table doesn't exist"
```bash
# Ejecuta las migraciones primero
python manage.py migrate
python manage.py loaddata db_export.json
```
