from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class MongoConnection:
    def __init__(self, host="localhost", port=27017, database="comerciotech_db"):
        self.host = host
        self.port = port
        self.database_name = database
        self.client = None
        self.db = None
        
    def connect(self):
        try:
            self.client = MongoClient(f"mongodb://{self.host}:{self.port}/")
            self.db = self.client[self.database_name]
            logger.info(f"Conexión exitosa a MongoDB: {self.database_name}")
            return True
        except Exception as e:
            logger.error(f"Error al conectar a MongoDB: {e}")
            return False

    def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Conexión a MongoDB cerrada")

    def validar_usuario(self, usuario, password):
        try:
            user_data = self.db.usuarios.find_one({"usuario": usuario, "password": password})
            return user_data is not None
        except Exception as e:
            logger.error(f"Error al validar usuario: {e}")
            return False

    # Operaciones CRUD para Clientes
    def crear_cliente(self, nombre, email, telefono, direccion):
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
        try:
            clientes = list(self.db.clientes.find())
            return clientes
        except Exception as e:
            logger.error(f"Error al obtener clientes: {e}")
            return []

    def obtener_cliente_por_id(self, cliente_id):
        try:
            return self.db.clientes.find_one({"_id": ObjectId(cliente_id)})
        except Exception as e:
            logger.error(f"Error al obtener cliente por ID: {e}")
            return None

    def actualizar_cliente(self, cliente_id, datos):
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
        try:
            result = self.db.clientes.delete_one({"_id": ObjectId(cliente_id)})
            logger.info(f"Cliente eliminado: {result.deleted_count} documento(s)")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar cliente: {e}")
            return False

    # Operaciones CRUD para Productos
    def crear_producto(self, nombre, descripcion, precio, stock, categoria):
        try:
            producto = {
                "nombre": nombre,
                "descripcion": descripcion,
                "precio": precio,
                "stock": stock,
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
        try:
            productos = list(self.db.productos.find())
            return productos
        except Exception as e:
            logger.error(f"Error al obtener productos: {e}")
            return []

    def obtener_producto_por_id(self, producto_id):
        try:
            return self.db.productos.find_one({"_id": ObjectId(producto_id)})
        except Exception as e:
            logger.error(f"Error al obtener producto por ID: {e}")
            return None

    def actualizar_producto(self, producto_id, datos):
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
        try:
            result = self.db.productos.delete_one({"_id": ObjectId(producto_id)})
            logger.info(f"Producto eliminado: {result.deleted_count} documento(s)")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar producto: {e}")
            return False

    # Operaciones CRUD para Pedidos
    def crear_pedido(self, id_cliente, productos_pedidos, direccion_envio, estado="Pendiente", total=0.0):
        try:
            pedido = {
                "id_cliente": ObjectId(id_cliente),
                "fecha_pedido": datetime.now(),
                "estado": estado,
                "total": total,
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
        try:
            # Realizar un lookup para obtener la información del cliente
            pedidos = list(self.db.pedidos.aggregate([
                {
                    "$lookup": {
                        "from": "clientes",
                        "localField": "id_cliente",
                        "foreignField": "_id",
                        "as": "cliente_info"
                    }
                },
                {
                    "$unwind": {
                        "path": "$cliente_info",
                        "preserveNullAndEmptyArrays": True
                    }
                    
                },
                {
                    "$lookup": {
                        "from": "productos",
                        "localField": "productos_pedidos.id_producto",
                        "foreignField": "_id",
                        "as": "productos_detalles"
                    }
                }
            ]))
            return pedidos
        except Exception as e:
            logger.error(f"Error al obtener pedidos: {e}")
            return []

    def obtener_pedido_por_id(self, pedido_id):
        try:
            # Realizar un lookup para obtener la información del cliente y productos
            pedido = list(self.db.pedidos.aggregate([
                {"$match": {"_id": ObjectId(pedido_id)}},
                {
                    "$lookup": {
                        "from": "clientes",
                        "localField": "id_cliente",
                        "foreignField": "_id",
                        "as": "cliente_info"
                    }
                },
                {
                    "$unwind": {
                        "path": "$cliente_info",
                        "preserveNullAndEmptyArrays": True
                    }
                },
                {
                    "$lookup": {
                        "from": "productos",
                        "localField": "productos_pedidos.id_producto",
                        "foreignField": "_id",
                        "as": "productos_detalles"
                    }
                }
            ]))
            return pedido[0] if pedido else None
        except Exception as e:
            logger.error(f"Error al obtener pedido por ID: {e}")
            return None

    def actualizar_pedido(self, pedido_id, datos):
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
        try:
            result = self.db.pedidos.delete_one({"_id": ObjectId(pedido_id)})
            logger.info(f"Pedido eliminado: {result.deleted_count} documento(s)")
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error al eliminar pedido: {e}")
            return False


