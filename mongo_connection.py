from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoConnection:
    def __init__(self, host='localhost', port=27017, database='comerciotech_db'):
        """
        Inicializa la conexión a MongoDB
        """
        self.host = host
        self.port = port
        self.database_name = database
        self.client = None
        self.db = None
        
    def connect(self):
        """
        Establece la conexión a MongoDB
        """
        try:
            self.client = MongoClient(f'mongodb://{self.host}:{self.port}/')
            self.db = self.client[self.database_name]
            logger.info(f"Conexión exitosa a MongoDB: {self.database_name}")
            return True
        except Exception as e:
            logger.error(f"Error al conectar a MongoDB: {e}")
            return False
    
    def disconnect(self):
        """
        Cierra la conexión a MongoDB
        """
        if self.client:
            self.client.close()
            logger.info("Conexión a MongoDB cerrada")
    
    def test_connection(self):
        """
        Prueba la conexión a MongoDB
        """
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            logger.error(f"Error en la prueba de conexión: {e}")
            return False
    
    # OPERACIONES CRUD PARA CLIENTES
    def crear_cliente(self, nombre, email, telefono, direccion):
        """
        Crea un nuevo cliente en la base de datos
        """
        try:
            cliente = {
                "nombre": nombre,
                "email": email,
                "telefono": telefono,
                "direccion": direccion,
                "fecha_registro": datetime.now()
            }
            result = self.db.clientes.insert_one(cliente)
            logger.info(f"Cliente creado con ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error al crear cliente: {e}")
            return None
    
    def obtener_clientes(self):
        """
        Obtiene todos los clientes de la base de datos
        """
        try:
            clientes = list(self.db.clientes.find())
            return clientes
        except Exception as e:
            logger.error(f"Error al obtener clientes: {e}")
            return []
    
    def actualizar_cliente(self, cliente_id, datos):
        """
        Actualiza un cliente existente
        """
        try:
            result = self.db.clientes.update_one(
                {"_id": ObjectId(cliente_id)},
                {"$set": datos}
            )
            logger.info(f"Cliente actualizado: {result.modified_count} documento(s)")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error al actualizar cliente: {e}")
            return False
    
    def eliminar_cliente(self, cliente_id):
        """
        Elimina un cliente de la base de datos
        """
        try:
            result = self.db.clientes.delete_one({"_id": ObjectId(cliente_id)})
            logger.info(f"Cliente eliminado: {result.deleted_count} documento(s)")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar cliente: {e}")
            return False
    
    # OPERACIONES CRUD PARA PRODUCTOS
    def crear_producto(self, nombre, descripcion, precio, stock, categoria):
        """
        Crea un nuevo producto en la base de datos
        """
        try:
            producto = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": float(precio),
                "stock": int(stock),
                "categoria": categoria,
                "fecha_creacion": datetime.now()
            }
            result = self.db.productos.insert_one(producto)
            logger.info(f"Producto creado con ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error al crear producto: {e}")
            return None
    
    def obtener_productos(self):
        """
        Obtiene todos los productos de la base de datos
        """
        try:
            productos = list(self.db.productos.find())
            return productos
        except Exception as e:
            logger.error(f"Error al obtener productos: {e}")
            return []
    
    def actualizar_producto(self, producto_id, datos):
        """
        Actualiza un producto existente
        """
        try:
            result = self.db.productos.update_one(
                {"_id": ObjectId(producto_id)},
                {"$set": datos}
            )
            logger.info(f"Producto actualizado: {result.modified_count} documento(s)")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error al actualizar producto: {e}")
            return False
    
    def eliminar_producto(self, producto_id):
        """
        Elimina un producto de la base de datos
        """
        try:
            result = self.db.productos.delete_one({"_id": ObjectId(producto_id)})
            logger.info(f"Producto eliminado: {result.deleted_count} documento(s)")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar producto: {e}")
            return False
    
    # OPERACIONES CRUD PARA PEDIDOS
    def crear_pedido(self, id_cliente, productos_pedidos, direccion_envio):
        """
        Crea un nuevo pedido en la base de datos
        """
        try:
            total = sum(item['cantidad'] * item['precio_unitario'] for item in productos_pedidos)
            
            pedido = {
                "id_cliente": ObjectId(id_cliente),
                "fecha_pedido": datetime.now(),
                "estado": "Pendiente",
                "total": float(total),
                "productos_pedidos": productos_pedidos,
                "direccion_envio": direccion_envio
            }
            result = self.db.pedidos.insert_one(pedido)
            logger.info(f"Pedido creado con ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            logger.error(f"Error al crear pedido: {e}")
            return None
    
    def obtener_pedidos(self):
        """
        Obtiene todos los pedidos de la base de datos con información del cliente
        """
        try:
            pipeline = [
                {
                    "$lookup": {
                        "from": "clientes",
                        "localField": "id_cliente",
                        "foreignField": "_id",
                        "as": "cliente_info"
                    }
                },
                {
                    "$unwind": "$cliente_info"
                }
            ]
            pedidos = list(self.db.pedidos.aggregate(pipeline))
            return pedidos
        except Exception as e:
            logger.error(f"Error al obtener pedidos: {e}")
            return []
    
    def actualizar_pedido(self, pedido_id, datos):
        """
        Actualiza un pedido existente
        """
        try:
            result = self.db.pedidos.update_one(
                {"_id": ObjectId(pedido_id)},
                {"$set": datos}
            )
            logger.info(f"Pedido actualizado: {result.modified_count} documento(s)")
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error al actualizar pedido: {e}")
            return False
    
    def eliminar_pedido(self, pedido_id):
        """
        Elimina un pedido de la base de datos
        """
        try:
            result = self.db.pedidos.delete_one({"_id": ObjectId(pedido_id)})
            logger.info(f"Pedido eliminado: {result.deleted_count} documento(s)")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar pedido: {e}")
            return False

    # FUNCIÓN DE VALIDACIÓN DE USUARIO (para login)
    def validar_usuario(self, usuario, password):
        """
        Valida las credenciales de un usuario
        """
        try:
            # Buscar usuario en la colección de usuarios
            user_data = self.db.usuarios.find_one({"usuario": usuario, "password": password})
            return user_data is not None
        except Exception as e:
            logger.error(f"Error al validar usuario: {e}")
            return False

