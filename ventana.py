from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QPushButton, QApplication, QTableWidgetItem, QDialog,
    QVBoxLayout, QFormLayout, QLineEdit, QDialogButtonBox,
    QMessageBox
)
import sys

class VentanaEditar(QDialog):
    def __init__(self, nombre="", apellido="", correo="", telefono="", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Usuario")
        self.resize(300, 200)

        self.nombreEdit = QLineEdit(nombre)
        self.apellidoEdit = QLineEdit(apellido)
        self.correoEdit = QLineEdit(correo)
        self.telefonoEdit = QLineEdit(telefono)

        formLayout = QFormLayout()
        formLayout.addRow("Nombre:", self.nombreEdit)
        formLayout.addRow("Apellido:", self.apellidoEdit)
        formLayout.addRow("Correo:", self.correoEdit)
        formLayout.addRow("Teléfono:", self.telefonoEdit)

        self.botones = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        self.botones.accepted.connect(self.accept)
        self.botones.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(self.botones)
        self.setLayout(layout)

    def getDatos(self):
        return (
            self.nombreEdit.text(),
            self.apellidoEdit.text(),
            self.correoEdit.text(),
            self.telefonoEdit.text()
        )

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ventana.ui', self)

        self.tablaUsuarios.setColumnCount(5)
        self.tablaUsuarios.setHorizontalHeaderLabels(['Nombre', 'Apellido', 'Correo', 'Teléfono', 'Acciones'])

        self.btnAgregar = self.findChild(QtWidgets.QPushButton, 'btnAgregar')
        self.btnAgregar.clicked.connect(self.agregar_usuario)

        self.datos = [
            ['Ana', 'Pérez', 'ana@example.com', '123456789'],
            ['Luis', 'Gómez', 'luis@example.com', '987654321']
        ]

        self.cargar_datos()

    def cargar_datos(self):
        self.tablaUsuarios.setRowCount(0)
        for fila, datos_fila in enumerate(self.datos):
            self.insertar_fila(fila, datos_fila)

    def insertar_fila(self, fila, datos_fila):
        self.tablaUsuarios.insertRow(fila)
        for col, valor in enumerate(datos_fila):
            self.tablaUsuarios.setItem(fila, col, QTableWidgetItem(valor))

        btnEditar = QPushButton('Editar')
        btnEditar.clicked.connect(lambda _, f=fila: self.editar(f))
        btnEliminar = QPushButton('Eliminar')
        btnEliminar.clicked.connect(lambda _, f=fila: self.eliminar(f))

        contenedor = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(btnEditar)
        layout.addWidget(btnEliminar)
        layout.setContentsMargins(0, 0, 0, 0)
        contenedor.setLayout(layout)

        self.tablaUsuarios.setCellWidget(fila, 4, contenedor)

    def editar(self, fila):
        datos_actuales = [self.tablaUsuarios.item(fila, i).text() for i in range(4)]
        dialogo = VentanaEditar(*datos_actuales, parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            nuevos_datos = dialogo.getDatos()
            for col, valor in enumerate(nuevos_datos):
                self.tablaUsuarios.setItem(fila, col, QTableWidgetItem(valor))
            self.datos[fila] = list(nuevos_datos)

    def eliminar(self, fila):
        nombre = self.tablaUsuarios.item(fila, 0).text()
        respuesta = QMessageBox.question(
            self,
            'Confirmar Eliminación',
            f'¿Estás seguro de eliminar a "{nombre}"?',
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.tablaUsuarios.removeRow(fila)
            self.datos.pop(fila)
            self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tablaUsuarios.setRowCount(0)
        for i, fila in enumerate(self.datos):
            self.insertar_fila(i, fila)

    def agregar_usuario(self):
        dialogo = VentanaEditar(parent=self)
        if dialogo.exec_() == QDialog.Accepted:
            nuevos_datos = dialogo.getDatos()
            self.datos.append(list(nuevos_datos))
            self.insertar_fila(len(self.datos) - 1, nuevos_datos)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    sys.exit(app.exec_())
