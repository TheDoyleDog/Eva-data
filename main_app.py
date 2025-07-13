from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QPushButton, QApplication, QTableWidgetItem, QDialog,
    QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox,
    QMessageBox, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit
)
from PyQt5.QtCore import Qt
from bson import ObjectId
from datetime import datetime
import sys

class ClienteDialog(QDialog):
    def __init__(self, cliente_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cliente")
        self.resize(400, 300)
        
        # Campos del formulario
        self.nombreEdit = QLineEdit(cliente_data.get('nombre', '') if cliente_data else '')
        self.emailEdit = QLineEdit(cliente_data.get('email', '') if cliente_data else '')
        self.telefonoEdit = QLineEdit(cliente_data.get('telefono', '') if cliente_data else '')
        
        # Campos de dirección
        direccion = cliente_data.get('direccion', {}) if cliente_data else {}
        self.calleEdit = QLineEdit(direccion.get('calle', ''))
        self.ciudadEdit = QLineEdit(direccion.get('ciudad', ''))
        self.provinciaEdit = QLineEdit(direccion.get('provincia', ''))
        self.codigoPostalEdit = QLineEdit(direccion.get('codigo_postal', ''))
        self.paisEdit = QLineEdit(direccion.get('pais', ''))
        
        # Layout del formulario
        formLayout = QFormLayout()
        formLayout.addRow("Nombre:", self.nombreEdit)
        formLayout.addRow("Email:", self.emailEdit)
        formLayout.addRow("Teléfono:", self.telefonoEdit)
        formLayout.addRow("Calle:", self.calleEdit)
        formLayout.addRow("Ciudad:", self.ciudadEdit)
        formLayout.addRow("Provincia:", self.provinciaEdit)
        formLayout.addRow("Código Postal:", self.codigoPostalEdit)
        formLayout.addRow("País:", self.paisEdit)
        
        # Botones
        self.botones = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(self.botones)
        self.setLayout(layout)
    
    def getDatos(self):
        return {
            'nombre': self.nombreEdit.text(),
            'email': self.emailEdit.text(),
            'telefono': self.telefonoEdit.text(),
            'direccion': {
                'calle': self.calleEdit.text(),
                'ciudad': self.ciudadEdit.text(),
                'provincia': self.provinciaEdit.text(),
                'codigo_postal': self.codigoPostalEdit.text(),
                'pais': self.paisEdit.text()
            }
        }

class ProductoDialog(QDialog):
    def __init__(self, producto_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Producto")
        self.resize(400, 250)
        
        # Campos del formulario
        self.nombreEdit = QLineEdit(producto_data.get('nombre', '') if producto_data else '')
        self.descripcionEdit = QTextEdit(producto_data.get('descripcion', '') if producto_data else '')
        self.precioEdit = QDoubleSpinBox()
        self.precioEdit.setMaximum(999999.99)
        self.precioEdit.setValue(producto_data.get('precio', 0.0) if producto_data else 0.0)
        
        self.stockEdit = QSpinBox()
        self.stockEdit.setMaximum(999999)
        self.stockEdit.setValue(producto_data.get('stock', 0) if producto_data else 0)
        
        self.categoriaEdit = QLineEdit(producto_data.get('categoria', '') if producto_data else '')
        
        # Layout del formulario
        formLayout = QFormLayout()
        formLayout.addRow("Nombre:", self.nombreEdit)
        formLayout.addRow("Descripción:", self.descripcionEdit)
        formLayout.addRow("Precio:", self.precioEdit)
        formLayout.addRow("Stock:", self.stockEdit)
        formLayout.addRow("Categoría:", self.categoriaEdit)
        
        # Botones
        self.botones = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        
        # Layout principal
        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(self.botones)
        self.setLayout(layout)
    
    def getDatos(self):
        return {
            'nombre': self.nombreEdit.text(),
            'descripcion': self.descripcionEdit.toPlainText(),
            'precio': self.precioEdit.value(),
            'stock': self.stockEdit.value(),
            'categoria': self.categoriaEdit.text()
        }

class MainApp(QtWidgets.QMainWindow):
    def __init__(self, mongo_connection):
        super().__init__()
        uic.loadUi('main_window.ui', self)
        
        self.mongo_conn = mongo_connection
        
        # Conectar botones
        self.btnAgregarCliente = self.findChild(QtWidgets.QPushButton, 'btnAgregarCliente')
        self.btnAgregarProducto = self.findChild(QtWidgets.QPushButton, 'btnAgregarProducto')
        self.btnAgregarPedido = self.findChild(QtWidgets.QPushButton, 'btnAgregarPedido')
        
        self.btnAgregarCliente.clicked.connect(self.agregar_cliente)
        self.btnAgregarProducto.clicked.connect(self.agregar_producto)
        self.btnAgregarPedido.clicked.connect(self.agregar_pedido)
        
        # Conectar tablas
        self.tablaClientes = self.findChild(QtWidgets.QTableWidget, 'tablaClientes')
        self.tablaProductos = self.findChild(QtWidgets.QTableWidget, 'tablaProductos')
        self.tablaPedidos = self.findChild(QtWidgets.QTableWidget, 'tablaPedidos')
        
        # Cargar datos iniciales
        self.cargar_clientes()
        self.cargar_productos()
        self.cargar_pedidos()
    
    def cargar_clientes(self):
        """
        Carga los clientes desde MongoDB y los muestra en la tabla
        """
        clientes = self.mongo_conn.obtener_clientes()
        self.tablaClientes.setRowCount(0)
        
        for fila, cliente in enumerate(clientes):
            self.tablaClientes.insertRow(fila)
            self.tablaClientes.setItem(fila, 0, QTableWidgetItem(cliente.get('nombre', '')))
            self.tablaClientes.setItem(fila, 1, QTableWidgetItem(cliente.get('email', '')))
            self.tablaClientes.setItem(fila, 2, QTableWidgetItem(cliente.get('telefono', '')))
            
            direccion = cliente.get('direccion', {})
            self.tablaClientes.setItem(fila, 3, QTableWidgetItem(direccion.get('ciudad', '')))
            
            fecha_registro = cliente.get('fecha_registro', '')
            if isinstance(fecha_registro, datetime):
                fecha_str = fecha_registro.strftime('%Y-%m-%d')
            else:
                fecha_str = str(fecha_registro)
            self.tablaClientes.setItem(fila, 4, QTableWidgetItem(fecha_str))
            
            # Botones de acción
            self.agregar_botones_accion_cliente(fila, str(cliente['_id']))
    
    def agregar_botones_accion_cliente(self, fila, cliente_id):
        """
        Agrega botones de editar y eliminar para cada cliente
        """
        btnEditar = QPushButton('Editar')
        btnEditar.clicked.connect(lambda _, id=cliente_id: self.editar_cliente(id))
        btnEliminar = QPushButton('Eliminar')
        btnEliminar.clicked.connect(lambda _, id=cliente_id: self.eliminar_cliente(id))
        
        contenedor = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(btnEditar)
        layout.addWidget(btnEliminar)
        layout.setContentsMargins(0, 0, 0, 0)
        contenedor.setLayout(layout)
        
        self.tablaClientes.setCellWidget(fila, 5, contenedor)
    
    def agregar_cliente(self):
        """
        Abre el diálogo para agregar un nuevo cliente
        """
        dialogo = ClienteDialog(parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.getDatos()
            if self.mongo_conn.crear_cliente(
                datos['nombre'], datos['email'], datos['telefono'], datos['direccion']
            ):
                self.cargar_clientes()
                self.mostrar_mensaje("Éxito", "Cliente agregado correctamente", QMessageBox.Information)
            else:
                self.mostrar_mensaje("Error", "No se pudo agregar el cliente", QMessageBox.Critical)
    
    def editar_cliente(self, cliente_id):
        """
        Abre el diálogo para editar un cliente existente
        """
        clientes = self.mongo_conn.obtener_clientes()
        cliente = next((c for c in clientes if str(c['_id']) == cliente_id), None)
        
        if cliente:
            dialogo = ClienteDialog(cliente, parent=self)
            if dialogo.exec_() == QDialog.Accepted:
                datos = dialogo.getDatos()
                if self.mongo_conn.actualizar_cliente(cliente_id, datos):
                    self.cargar_clientes()
                    self.mostrar_mensaje("Éxito", "Cliente actualizado correctamente", QMessageBox.Information)
                else:
                    self.mostrar_mensaje("Error", "No se pudo actualizar el cliente", QMessageBox.Critical)
    
    def eliminar_cliente(self, cliente_id):
        """
        Elimina un cliente después de confirmar
        """
        respuesta = QMessageBox.question(
            self, 'Confirmar Eliminación',
            '¿Estás seguro de eliminar este cliente?',
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            if self.mongo_conn.eliminar_cliente(cliente_id):
                self.cargar_clientes()
                self.mostrar_mensaje("Éxito", "Cliente eliminado correctamente", QMessageBox.Information)
            else:
                self.mostrar_mensaje("Error", "No se pudo eliminar el cliente", QMessageBox.Critical)
    
    def cargar_productos(self):
        """
        Carga los productos desde MongoDB y los muestra en la tabla
        """
        productos = self.mongo_conn.obtener_productos()
        self.tablaProductos.setRowCount(0)
        
        for fila, producto in enumerate(productos):
            self.tablaProductos.insertRow(fila)
            self.tablaProductos.setItem(fila, 0, QTableWidgetItem(producto.get('nombre', '')))
            self.tablaProductos.setItem(fila, 1, QTableWidgetItem(producto.get('descripcion', '')))
            self.tablaProductos.setItem(fila, 2, QTableWidgetItem(f"${producto.get('precio', 0):.2f}"))
            self.tablaProductos.setItem(fila, 3, QTableWidgetItem(str(producto.get('stock', 0))))
            self.tablaProductos.setItem(fila, 4, QTableWidgetItem(producto.get('categoria', '')))
            
            # Botones de acción
            self.agregar_botones_accion_producto(fila, str(producto['_id']))
    
    def agregar_botones_accion_producto(self, fila, producto_id):
        """
        Agrega botones de editar y eliminar para cada producto
        """
        btnEditar = QPushButton('Editar')
        btnEditar.clicked.connect(lambda _, id=producto_id: self.editar_producto(id))
        btnEliminar = QPushButton('Eliminar')
        btnEliminar.clicked.connect(lambda _, id=producto_id: self.eliminar_producto(id))
        
        contenedor = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(btnEditar)
        layout.addWidget(btnEliminar)
        layout.setContentsMargins(0, 0, 0, 0)
        contenedor.setLayout(layout)
        
        self.tablaProductos.setCellWidget(fila, 5, contenedor)
    
    def agregar_producto(self):
        """
        Abre el diálogo para agregar un nuevo producto
        """
        dialogo = ProductoDialog(parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            datos = dialogo.getDatos()
            if self.mongo_conn.crear_producto(
                datos['nombre'], datos['descripcion'], datos['precio'], 
                datos['stock'], datos['categoria']
            ):
                self.cargar_productos()
                self.mostrar_mensaje("Éxito", "Producto agregado correctamente", QMessageBox.Information)
            else:
                self.mostrar_mensaje("Error", "No se pudo agregar el producto", QMessageBox.Critical)
    
    def editar_producto(self, producto_id):
        """
        Abre el diálogo para editar un producto existente
        """
        productos = self.mongo_conn.obtener_productos()
        producto = next((p for p in productos if str(p['_id']) == producto_id), None)
        
        if producto:
            dialogo = ProductoDialog(producto, parent=self)
            if dialogo.exec_() == QDialog.Accepted:
                datos = dialogo.getDatos()
                if self.mongo_conn.actualizar_producto(producto_id, datos):
                    self.cargar_productos()
                    self.mostrar_mensaje("Éxito", "Producto actualizado correctamente", QMessageBox.Information)
                else:
                    self.mostrar_mensaje("Error", "No se pudo actualizar el producto", QMessageBox.Critical)
    
    def eliminar_producto(self, producto_id):
        """
        Elimina un producto después de confirmar
        """
        respuesta = QMessageBox.question(
            self, 'Confirmar Eliminación',
            '¿Estás seguro de eliminar este producto?',
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            if self.mongo_conn.eliminar_producto(producto_id):
                self.cargar_productos()
                self.mostrar_mensaje("Éxito", "Producto eliminado correctamente", QMessageBox.Information)
            else:
                self.mostrar_mensaje("Error", "No se pudo eliminar el producto", QMessageBox.Critical)
    
    def cargar_pedidos(self):
        """
        Carga los pedidos desde MongoDB y los muestra en la tabla
        """
        pedidos = self.mongo_conn.obtener_pedidos()
        self.tablaPedidos.setRowCount(0)
        
        for fila, pedido in enumerate(pedidos):
            self.tablaPedidos.insertRow(fila)
            self.tablaPedidos.setItem(fila, 0, QTableWidgetItem(str(pedido['_id'])))
            
            cliente_info = pedido.get('cliente_info', {})
            self.tablaPedidos.setItem(fila, 1, QTableWidgetItem(cliente_info.get('nombre', '')))
            
            fecha_pedido = pedido.get('fecha_pedido', '')
            if isinstance(fecha_pedido, datetime):
                fecha_str = fecha_pedido.strftime('%Y-%m-%d %H:%M')
            else:
                fecha_str = str(fecha_pedido)
            self.tablaPedidos.setItem(fila, 2, QTableWidgetItem(fecha_str))
            
            self.tablaPedidos.setItem(fila, 3, QTableWidgetItem(pedido.get('estado', '')))
            self.tablaPedidos.setItem(fila, 4, QTableWidgetItem(f"${pedido.get('total', 0):.2f}"))
            
            # Botones de acción
            self.agregar_botones_accion_pedido(fila, str(pedido['_id']))
    
    def agregar_botones_accion_pedido(self, fila, pedido_id):
        """
        Agrega botones de ver y eliminar para cada pedido
        """
        btnVer = QPushButton('Ver')
        btnVer.clicked.connect(lambda _, id=pedido_id: self.ver_pedido(id))
        btnEliminar = QPushButton('Eliminar')
        btnEliminar.clicked.connect(lambda _, id=pedido_id: self.eliminar_pedido(id))
        
        contenedor = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(btnVer)
        layout.addWidget(btnEliminar)
        layout.setContentsMargins(0, 0, 0, 0)
        contenedor.setLayout(layout)
        
        self.tablaPedidos.setCellWidget(fila, 5, contenedor)
    
    def agregar_pedido(self):
        """
        Funcionalidad básica para agregar pedido (simplificada)
        """
        self.mostrar_mensaje("Información", "Funcionalidad de agregar pedido en desarrollo", QMessageBox.Information)
    
    def ver_pedido(self, pedido_id):
        """
        Muestra los detalles de un pedido
        """
        self.mostrar_mensaje("Información", f"Ver detalles del pedido: {pedido_id}", QMessageBox.Information)
    
    def eliminar_pedido(self, pedido_id):
        """
        Elimina un pedido después de confirmar
        """
        respuesta = QMessageBox.question(
            self, 'Confirmar Eliminación',
            '¿Estás seguro de eliminar este pedido?',
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            if self.mongo_conn.eliminar_pedido(pedido_id):
                self.cargar_pedidos()
                self.mostrar_mensaje("Éxito", "Pedido eliminado correctamente", QMessageBox.Information)
            else:
                self.mostrar_mensaje("Error", "No se pudo eliminar el pedido", QMessageBox.Critical)
    
    def mostrar_mensaje(self, titulo, mensaje, tipo):
        """
        Muestra un mensaje al usuario
        """
        msgBox = QMessageBox()
        msgBox.setIcon(tipo)
        msgBox.setText(mensaje)
        msgBox.setWindowTitle(titulo)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Para pruebas directas
    from mongo_connection import MongoConnection
    mongo_conn = MongoConnection()
    mongo_conn.connect()
    window = MainApp(mongo_conn)
    window.show()
    sys.exit(app.exec_())

