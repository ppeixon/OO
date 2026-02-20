# Gestión de Órdenes de Servicio (CRUD)

Aplicación web sencilla para gestionar órdenes de servicio con base de datos SQL (SQLite) en lugar de Excel.

## Qué incluye
- Crear órdenes de servicio.
- Listar y buscar órdenes por referencia, empresa o descripción.
- Editar órdenes existentes.
- Eliminar órdenes.
- Interfaz web simple y guiada.

## Stack
- Python 3
- Flask
- SQLite

## Estructura
- `app.py`: aplicación principal y rutas CRUD.
- `templates/`: vistas HTML.
- `static/styles.css`: estilos básicos.
- `service_orders.db`: base de datos SQLite (se crea automáticamente al iniciar).

## Cómo ejecutar
1. Crear entorno virtual (opcional pero recomendado):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar la app:
   ```bash
   flask --app app run
   ```
4. Abrir en navegador:
   `http://127.0.0.1:5000`

## Campos de la orden de servicio
- Referencia (única)
- Empresa
- Descripción
- Estado (`Pendiente`, `En progreso`, `Completada`, `Cancelada`)
- Fecha de creación (automática)

## Próximos pasos recomendados
- Autenticación de usuarios y permisos.
- Exportación a Excel/PDF para reportes.
- Recordatorios automáticos por correo.
- Dashboard con KPIs (órdenes por estado, tiempos de cierre, etc.).
