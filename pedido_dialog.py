from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QDialogButtonBox,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QMessageBox,
    QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt
from bson import ObjectId
from datetime import datetime

class PedidoDialog(QDialog):
    def __init__(self, mongo_conn, pedido_data=None, parent=None):
        super().__init__(parent)
        self.mongo_conn = mongo_conn
        self.pedido_data = pedido_data
        self.productos_pedido = []
        
        self.setWindowTitle("Pedido")
        self.resize(700, 600)
        
        self.init_ui()
        
        if pedido_data:
            self.cargar_datos_pedido()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Información del cliente
        cliente_group = QGroupBox("Información del Cliente")
        cliente_layout = QFormLayout()
        
        self.clienteCombo = QComboBox()
        self.cargar_clientes()
        cliente_layout.addRow("Cliente:", self.clienteCombo)
        
        cliente_group.setLayout(cliente_layout)
        layout.addWidget(cliente_group)
        
        # Información del pedido
        pedido_group = QGroupBox("Información del Pedido")
        pedido_layout = QFormLayout()
        
        self.estadoCombo = QComboBox()
        self.estadoCombo.addItems(["Pendiente", "Procesando", "Enviado", "Entregado", "Cancelado"])
        pedido_layout.addRow("Estado:", self.estadoCombo)
        
        pedido_group.setLayout(pedido_layout)
        layout.addWidget(pedido_group)
        
        # Dirección de envío
        direccion_group = QGroupBox("Dirección de Envío")
        direccion_layout = QFormLayout()
        
        self.calleEdit = QLineEdit()
        self.ciudadEdit = QLineEdit()
        self.provinciaEdit = QLineEdit()
        self.codigoPostalEdit = QLineEdit()
        self.paisEdit = QLineEdit()
        
        direccion_layout.addRow("Calle:", self.calleEdit)
        direccion_layout.addRow("Ciudad:", self.ciudadEdit)
        direccion_layout.addRow("Provincia:", self.provinciaEdit)
        direccion_layout.addRow("Código Postal:", self.codigoPostalEdit)
        direccion_layout.addRow("País:", self.paisEdit)
        
        direccion_group.setLayout(direccion_layout)
        layout.addWidget(direccion_group)
        
        # Productos del pedido
        productos_group = QGroupBox("Productos del Pedido")
        productos_layout = QVBoxLayout()
        
        # Botón para agregar productos
        btn_layout = QHBoxLayout()
        self.btnAgregarProducto = QPushButton("Agregar Producto")
        self.btnAgregarProducto.clicked.connect(self.agregar_producto)
        btn_layout.addWidget(self.btnAgregarProducto)
        btn_layout.addStretch()
        productos_layout.addLayout(btn_layout)
        
        # Tabla de productos
        self.tablaProductos = QTableWidget()
        self.tablaProductos.setColumnCount(5)
        self.tablaProductos.setHorizontalHeaderLabels([
            "Producto", "Precio Unitario", "Cantidad", "Subtotal", "Acciones"
        ])
        productos_layout.addWidget(self.tablaProductos)
        
        # Total
        total_layout = QHBoxLayout()
        total_layout.addStretch()
        self.labelTotal = QLabel("Total: $0.00")
        self.labelTotal.setStyleSheet("font-weight: bold; font-size: 14px;")
        total_layout.addWidget(self.labelTotal)
        productos_layout.addLayout(total_layout)
        
        productos_group.setLayout(productos_layout)
        layout.addWidget(productos_group)
        
        # Botones del diálogo
        self.botones = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botones.button(QDialogButtonBox.Save).setText("Guardar")
        self.botones.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        layout.addWidget(self.botones)
        
        self.setLayout(layout)
    
    def cargar_clientes(self):
        """Carga la lista de clientes en el combo box"""
        clientes = self.mongo_conn.obtener_clientes()
        self.clienteCombo.clear()
        
        for cliente in clientes:
            self.clienteCombo.addItem(
                f"{cliente['nombre']} ({cliente['email']})",
                str(cliente['_id'])
            )
    
    def agregar_producto(self):
        """Abre el diálogo para agregar un producto al pedido"""
        dialog = ProductoPedidoDialog(self.mongo_conn, parent=self)
        if dialog.exec_() == QDialog.Accepted:
            producto_data = dialog.getDatos()
            self.productos_pedido.append(producto_data)
            self.actualizar_tabla_productos()
            self.calcular_total()
    
    def actualizar_tabla_productos(self):
        """Actualiza la tabla de productos del pedido"""
        self.tablaProductos.setRowCount(0)
        
        for fila, producto in enumerate(self.productos_pedido):
            self.tablaProductos.insertRow(fila)
            
            # Obtener información del producto
            producto_info = self.mongo_conn.obtener_producto_por_id(producto['id_producto'])
            nombre_producto = producto_info['nombre'] if producto_info else "Producto no encontrado"
            
            self.tablaProductos.setItem(fila, 0, QTableWidgetItem(nombre_producto))
            self.tablaProductos.setItem(fila, 1, QTableWidgetItem(f"${producto['precio_unitario']:.2f}"))
            self.tablaProductos.setItem(fila, 2, QTableWidgetItem(str(producto['cantidad'])))
            
            subtotal = producto['precio_unitario'] * producto['cantidad']
            self.tablaProductos.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))
            
            # Botón eliminar
            btnEliminar = QPushButton("Eliminar")
            btnEliminar.clicked.connect(lambda _, f=fila: self.eliminar_producto(f))
            self.tablaProductos.setCellWidget(fila, 4, btnEliminar)
    
    def eliminar_producto(self, fila):
        """Elimina un producto del pedido"""
        if 0 <= fila < len(self.productos_pedido):
            self.productos_pedido.pop(fila)
            self.actualizar_tabla_productos()
            self.calcular_total()
    
    def calcular_total(self):
        """Calcula y muestra el total del pedido"""
        total = sum(p['precio_unitario'] * p['cantidad'] for p in self.productos_pedido)
        self.labelTotal.setText(f"Total: ${total:.2f}")
    
    def cargar_datos_pedido(self):
        """Carga los datos de un pedido existente para edición"""
        if not self.pedido_data:
            return
        
        # Seleccionar cliente
        cliente_id = str(self.pedido_data.get('id_cliente', ''))
        for i in range(self.clienteCombo.count()):
            if self.clienteCombo.itemData(i) == cliente_id:
                self.clienteCombo.setCurrentIndex(i)
                break
        
        # Estado
        estado = self.pedido_data.get('estado', 'Pendiente')
        index = self.estadoCombo.findText(estado)
        if index >= 0:
            self.estadoCombo.setCurrentIndex(index)
        
        # Dirección de envío
        direccion = self.pedido_data.get('direccion_envio', {})
        self.calleEdit.setText(direccion.get('calle', ''))
        self.ciudadEdit.setText(direccion.get('ciudad', ''))
        self.provinciaEdit.setText(direccion.get('provincia', ''))
        self.codigoPostalEdit.setText(direccion.get('codigo_postal', ''))
        self.paisEdit.setText(direccion.get('pais', ''))
        
        # Productos del pedido
        self.productos_pedido = self.pedido_data.get('productos_pedidos', [])
        self.actualizar_tabla_productos()
        self.calcular_total()
    
    def getDatos(self):
        """Retorna los datos del pedido"""
        direccion_envio = {
            "calle": self.calleEdit.text(),
            "ciudad": self.ciudadEdit.text(),
            "provincia": self.provinciaEdit.text(),
            "codigo_postal": self.codigoPostalEdit.text(),
            "pais": self.paisEdit.text()
        }
        
        total = sum(p['precio_unitario'] * p['cantidad'] for p in self.productos_pedido)
        
        return {
            "id_cliente": self.clienteCombo.currentData(),
            "estado": self.estadoCombo.currentText(),
            "productos_pedidos": self.productos_pedido,
            "direccion_envio": direccion_envio,
            "total": total
        }

class ProductoPedidoDialog(QDialog):
    def __init__(self, mongo_conn, parent=None):
        super().__init__(parent)
        self.mongo_conn = mongo_conn
        
        self.setWindowTitle("Agregar Producto al Pedido")
        self.resize(400, 200)
        
        layout = QFormLayout()
        
        # Combo de productos
        self.productoCombo = QComboBox()
        self.cargar_productos()
        layout.addRow("Producto:", self.productoCombo)
        
        # Cantidad
        self.cantidadSpinBox = QSpinBox()
        self.cantidadSpinBox.setMinimum(1)
        self.cantidadSpinBox.setMaximum(1000)
        self.cantidadSpinBox.setValue(1)
        layout.addRow("Cantidad:", self.cantidadSpinBox)
        
        # Precio unitario (se llena automáticamente)
        self.precioLabel = QLabel("$0.00")
        layout.addRow("Precio Unitario:", self.precioLabel)
        
        # Conectar cambio de producto para actualizar precio
        self.productoCombo.currentIndexChanged.connect(self.actualizar_precio)
        self.actualizar_precio()  # Inicializar precio
        
        # Botones
        self.botones = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.botones.button(QDialogButtonBox.Ok).setText("Aceptar")
        self.botones.button(QDialogButtonBox.Cancel).setText("Cancelar")
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)
        layout.addWidget(self.botones)
        
        self.setLayout(layout)
    
    def cargar_productos(self):
        """Carga la lista de productos en el combo box"""
        productos = self.mongo_conn.obtener_productos()
        self.productoCombo.clear()
        
        for producto in productos:
            self.productoCombo.addItem(
                f"{producto['nombre']} (Stock: {producto['stock']})",
                {
                    "id": str(producto["_id"]),
                    "precio": producto["precio"],
                    "stock": producto["stock"]
                }
            )
    
    def actualizar_precio(self):
        """Actualiza el precio mostrado según el producto seleccionado"""
        data = self.productoCombo.currentData()
        if data:
            self.precioLabel.setText(f"${data['precio']:.2f}")
    
    def getDatos(self):
        """Retorna los datos del producto para el pedido"""
        data = self.productoCombo.currentData()
        if not data:
            return None
        
        return {
            "id_producto": ObjectId(data["id"]),
            "cantidad": self.cantidadSpinBox.value(),
            "precio_unitario": data["precio"]
        }

class PedidoDetalleDialog(QDialog):
    def __init__(self, mongo_conn, pedido_id, parent=None):
        super().__init__(parent)
        self.mongo_conn = mongo_conn
        self.pedido_id = pedido_id
        
        self.setWindowTitle("Detalles del Pedido")
        self.resize(600, 500)
        
        self.init_ui()
        self.cargar_detalles()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Información general
        info_group = QGroupBox("Información General")
        info_layout = QFormLayout()
        
        self.labelId = QLabel()
        self.labelCliente = QLabel()
        self.labelFecha = QLabel()
        self.labelEstado = QLabel()
        self.labelTotal = QLabel()
        
        info_layout.addRow("ID Pedido:", self.labelId)
        info_layout.addRow("Cliente:", self.labelCliente)
        info_layout.addRow("Fecha:", self.labelFecha)
        info_layout.addRow("Estado:", self.labelEstado)
        info_layout.addRow("Total:", self.labelTotal)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Dirección de envío
        direccion_group = QGroupBox("Dirección de Envío")
        self.labelDireccion = QLabel()
        self.labelDireccion.setWordWrap(True)
        direccion_layout = QVBoxLayout()
        direccion_layout.addWidget(self.labelDireccion)
        direccion_group.setLayout(direccion_layout)
        layout.addWidget(direccion_group)
        
        # Productos
        productos_group = QGroupBox("Productos del Pedido")
        productos_layout = QVBoxLayout()
        
        self.tablaProductos = QTableWidget()
        self.tablaProductos.setColumnCount(4)
        self.tablaProductos.setHorizontalHeaderLabels([
            "Producto", "Precio Unitario", "Cantidad", "Subtotal"
        ])
        productos_layout.addWidget(self.tablaProductos)
        
        productos_group.setLayout(productos_layout)
        layout.addWidget(productos_group)
        
        # Botón cerrar
        self.btnCerrar = QPushButton("Cerrar")
        self.btnCerrar.clicked.connect(self.accept)
        layout.addWidget(self.btnCerrar)
        
        self.setLayout(layout)
    
    def cargar_detalles(self):
        """Carga los detalles del pedido"""
        pedido = self.mongo_conn.obtener_pedido_por_id(self.pedido_id)
        if not pedido:
            QMessageBox.warning(self, "Error", "No se pudo cargar el pedido")
            return
        
        # Información general
        self.labelId.setText(str(pedido["_id"]))
        
        cliente_info = pedido.get('cliente_info', {})
        self.labelCliente.setText(f"{cliente_info.get('nombre', '')} ({cliente_info.get('email', '')})")
        
        fecha_pedido = pedido.get('fecha_pedido', '')
        if isinstance(fecha_pedido, datetime):
            fecha_str = fecha_pedido.strftime("%Y-%m-%d %H:%M:%S")
        else:
            fecha_str = str(fecha_pedido)
        self.labelFecha.setText(fecha_str)
        
        self.labelEstado.setText(pedido.get('estado', ''))
        self.labelTotal.setText(f"${pedido.get('total', 0):.2f}")
        
        # Dirección de envío
        direccion = pedido.get('direccion_envio', {})
        direccion_texto = f"{direccion.get('calle', '')}\n"
        direccion_texto += f"{direccion.get('ciudad', '')}, {direccion.get('provincia', '')}\n"
        direccion_texto += f"{direccion.get('codigo_postal', '')} - {direccion.get('pais', '')}"
        self.labelDireccion.setText(direccion_texto)
        
        # Productos
        productos_pedidos = pedido.get('productos_pedidos', [])
        self.tablaProductos.setRowCount(len(productos_pedidos))
        
        for fila, producto_pedido in enumerate(productos_pedidos):
            # Obtener información del producto
            producto_info = self.mongo_conn.obtener_producto_por_id(producto_pedido['id_producto'])
            nombre_producto = producto_info['nombre'] if producto_info else "Producto no encontrado"
            
            self.tablaProductos.setItem(fila, 0, QTableWidgetItem(nombre_producto))
            self.tablaProductos.setItem(fila, 1, QTableWidgetItem(f"${producto_pedido['precio_unitario']:.2f}"))
            self.tablaProductos.setItem(fila, 2, QTableWidgetItem(str(producto_pedido['cantidad'])))
            
            subtotal = producto_pedido['precio_unitario'] * producto_pedido['cantidad']
            self.tablaProductos.setItem(fila, 3, QTableWidgetItem(f"${subtotal:.2f}"))




