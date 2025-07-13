# ComercioTech - Sistema de Gestión

## Descripción
ComercioTech es una aplicación de escritorio desarrollada con PyQt5 que permite gestionar clientes, productos y pedidos utilizando MongoDB como base de datos no estructurada.

## Requisitos del Sistema

### Software Necesario
- Python 3.7 o superior
- MongoDB 4.0 o superior
- MongoDB Compass (opcional, para gestión visual de la base de datos)

### Dependencias de Python
```bash
pip install PyQt5 pymongo
```

## Configuración de la Base de Datos

### 1. Instalación de MongoDB
- Descargar e instalar MongoDB desde: https://www.mongodb.com/try/download/community
- Iniciar el servicio de MongoDB
- Por defecto, MongoDB se ejecuta en `localhost:27017`

### 2. Configuración de la Base de Datos
La aplicación utiliza la base de datos `comerciotech_db` con las siguientes colecciones:

#### Colecciones:
- **usuarios**: Para autenticación del sistema
- **clientes**: Información de clientes
- **productos**: Catálogo de productos
- **pedidos**: Órdenes de compra

### 3. Importar Datos de Ejemplo

#### Usando MongoDB Compass:
1. Abrir MongoDB Compass
2. Conectar a `mongodb://localhost:27017`
3. Crear la base de datos `comerciotech_db`
4. Importar los archivos JSON en sus respectivas colecciones:
   - `usuarios.json` → colección `usuarios`
   - `clientes.json` → colección `clientes`
   - `productos.json` → colección `productos`
   - `pedidos.json` → colección `pedidos`

#### Usando MongoDB Shell:
```bash
# Conectar a MongoDB
mongo

# Usar la base de datos
use comerciotech_db

# Importar usuarios
mongoimport --db comerciotech_db --collection usuarios --file usuarios.json --jsonArray

# Importar clientes
mongoimport --db comerciotech_db --collection clientes --file clientes.json --jsonArray

# Importar productos
mongoimport --db comerciotech_db --collection productos --file productos.json --jsonArray

# Importar pedidos (después de importar clientes y productos)
mongoimport --db comerciotech_db --collection pedidos --file pedidos.json --jsonArray
```

**Nota Importante**: Para el archivo `pedidos.json`, debes reemplazar los marcadores `<ObjectId_del_cliente_X>` y `<ObjectId_del_producto_X>` con los `_id` reales de los documentos de clientes y productos después de importarlos.

## Estructura del Proyecto

```
comerciotech_app/
├── login.ui                 # Interfaz de login (QtDesigner)
├── main_window.ui          # Interfaz principal (QtDesigner)
├── login_app.py            # Aplicación de login
├── main_app.py             # Aplicación principal
├── mongo_connection.py     # Conexión y operaciones MongoDB
├── usuarios.json           # Datos de usuarios para login
├── clientes.json           # Datos de ejemplo de clientes
├── productos.json          # Datos de ejemplo de productos
├── pedidos.json            # Datos de ejemplo de pedidos
└── README.md               # Este archivo
```

## Uso de la Aplicación

### 1. Ejecutar la Aplicación
```bash
cd comerciotech_app
python login_app.py
```

### 2. Credenciales de Acceso
- **Usuario**: admin
- **Contraseña**: admin123

O también:
- **Usuario**: usuario1
- **Contraseña**: pass123

### 3. Funcionalidades

#### Gestión de Clientes
- Agregar nuevos clientes
- Editar información de clientes existentes
- Eliminar clientes
- Visualizar lista completa de clientes

#### Gestión de Productos
- Agregar nuevos productos
- Editar información de productos
- Eliminar productos
- Visualizar catálogo de productos

#### Gestión de Pedidos
- Visualizar pedidos existentes
- Ver detalles de pedidos
- Eliminar pedidos
- (Funcionalidad de agregar pedidos en desarrollo)

## Operaciones CRUD Implementadas

### Clientes
- **Create**: Agregar nuevo cliente con información completa
- **Read**: Listar todos los clientes
- **Update**: Modificar información de cliente existente
- **Delete**: Eliminar cliente del sistema

### Productos
- **Create**: Agregar nuevo producto al catálogo
- **Read**: Listar todos los productos
- **Update**: Modificar información de producto
- **Delete**: Eliminar producto del catálogo

### Pedidos
- **Read**: Listar pedidos con información del cliente
- **Delete**: Eliminar pedidos
- (Create y Update en desarrollo)

## Características Técnicas

### Base de Datos MongoDB
- Uso de colecciones no estructuradas
- Relaciones mediante ObjectId
- Agregaciones para consultas complejas
- Índices automáticos en _id

### Interfaz Gráfica
- Desarrollada con PyQt5 y QtDesigner
- Interfaces responsivas y amigables
- Diálogos modales para formularios
- Tablas dinámicas con botones de acción

### Seguridad
- Autenticación de usuarios
- Validación de datos de entrada
- Manejo de errores y excepciones
- Logging de operaciones

## Solución de Problemas

### Error de Conexión a MongoDB
- Verificar que MongoDB esté ejecutándose
- Comprobar la dirección y puerto (localhost:27017)
- Verificar permisos de acceso

### Error de Dependencias
```bash
pip install --upgrade PyQt5 pymongo
```

### Error de Interfaz Gráfica
- Verificar que los archivos .ui estén en el directorio correcto
- Comprobar que PyQt5 esté instalado correctamente

## Desarrollo Futuro

### Funcionalidades Pendientes
- Completar gestión de pedidos (agregar y editar)
- Reportes y estadísticas
- Búsqueda y filtros avanzados
- Exportación de datos
- Gestión de usuarios y roles

### Mejoras Técnicas
- Implementar patrones de diseño (MVC)
- Agregar pruebas unitarias
- Mejorar manejo de errores
- Optimizar consultas a la base de datos

## Contacto y Soporte

Para soporte técnico o consultas sobre la aplicación, contactar al equipo de desarrollo de ComercioTech.

