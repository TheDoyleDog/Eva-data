# ComercioTech - Sistema de Gestión Corregido

## Descripción

Esta es la versión corregida del sistema ComercioTech que incluye:
- Login sin mensajes por terminal
- Ventana principal con gestión CRUD completa
- Interfaz con pestañas para Clientes, Productos y Pedidos
- Operaciones completas de Crear, Leer, Actualizar y Eliminar

## Archivos Principales

### Aplicación
- `app.py` - Aplicación principal con login
- `ventana.py` - Ventana principal con interfaz CRUD
- `login.ui` - Interfaz de login (QtDesigner)
- `ventana.ui` - Interfaz principal (QtDesigner)

### Conexión a Base de Datos
- `libreria_mongo.py` - Función de validación de usuario (original)
- `mongo_connection.py` - Clase completa para operaciones CRUD

### Datos
- `usuarios.json` - Usuarios del sistema
- `clientes.json` - Datos de clientes
- `productos.json` - Datos de productos
- `pedidos.json` - Datos de pedidos

## Credenciales de Acceso

- **Usuario**: admin | **Contraseña**: admin123
- **Usuario**: usuario1 | **Contraseña**: pass123

## Instalación y Uso

### 1. Requisitos
```bash
pip install PyQt5 pymongo
```

### 2. MongoDB
Asegúrate de que MongoDB esté ejecutándose:
```bash
sudo systemctl start mongod
```

### 3. Importar Datos
```bash
mongoimport --db comerciotech_db --collection usuarios --file usuarios.json --jsonArray
mongoimport --db comerciotech_db --collection clientes --file clientes.json --jsonArray
mongoimport --db comerciotech_db --collection productos --file productos.json --jsonArray
```

### 4. Ejecutar Aplicación
```bash
python3 app.py
```

## Funcionalidades

### Login
- Validación de credenciales contra MongoDB
- Sin mensajes por terminal
- Transición automática a ventana principal

### Gestión de Clientes
- ✅ Agregar nuevos clientes
- ✅ Editar información de clientes
- ✅ Eliminar clientes
- ✅ Visualizar lista de clientes

### Gestión de Productos
- ✅ Agregar nuevos productos
- ✅ Editar información de productos
- ✅ Eliminar productos
- ✅ Visualizar catálogo de productos

### Gestión de Pedidos
- ✅ Visualizar pedidos existentes
- ✅ Ver detalles de pedidos
- ✅ Eliminar pedidos
- ⚠️ Agregar pedidos (funcionalidad básica)

## Cambios Realizados

### Correcciones en el Login
1. Eliminados todos los `print()` que mostraban mensajes por terminal
2. Agregada transición automática a ventana principal después del login exitoso
3. Integración con la nueva clase `MongoConnection`

### Nueva Ventana Principal
1. Interfaz con pestañas para cada tipo de dato
2. Tablas con datos cargados desde MongoDB
3. Botones de acción (Agregar, Editar, Eliminar) para cada registro
4. Diálogos modales para formularios de entrada

### Operaciones CRUD Completas
1. Clase `MongoConnection` con todas las operaciones necesarias
2. Validación de datos en formularios
3. Mensajes de confirmación y error
4. Actualización automática de tablas después de operaciones

## Estructura de la Base de Datos

### Colecciones
- `usuarios` - Autenticación del sistema
- `clientes` - Información de clientes con direcciones
- `productos` - Catálogo de productos con precios y stock
- `pedidos` - Órdenes de compra con relaciones a clientes

### Relaciones
- Clientes ↔ Pedidos (Uno a muchos)
- Productos ↔ Pedidos (Muchos a muchos)

## Notas Técnicas

- La aplicación requiere un entorno gráfico para ejecutar PyQt5
- MongoDB debe estar ejecutándose en localhost:27017
- Los archivos .ui deben estar en el mismo directorio que los archivos .py
- La base de datos debe llamarse exactamente `comerciotech_db`

## Solución de Problemas

### Error: "No se puede conectar a MongoDB"
```bash
sudo systemctl status mongod
sudo systemctl start mongod
```

### Error: "ModuleNotFoundError: No module named 'PyQt5'"
```bash
pip install PyQt5
```

### Error: "qt.qpa.plugin: Could not load the Qt platform plugin"
Esto indica que no hay un entorno gráfico disponible. La aplicación necesita ejecutarse en un sistema con interfaz gráfica.

---

¡La aplicación ComercioTech está lista para usar con todas las funcionalidades CRUD implementadas!

