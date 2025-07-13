from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import libreria_mongo as miLib
from mongo_connection import MongoConnection # Importar la nueva clase de conexión
import sys

# Importar la nueva ventana principal
from ventana import MainApp

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("login.ui", self)
        self.adjustSize()

        self.show()

        self.ingreso = self.findChild(QtWidgets.QPushButton, "btnIngresar")
        self.salida = self.findChild(QtWidgets.QPushButton, "btnSalir")

        self.usr = self.findChild(QtWidgets.QLineEdit, "inputUsuario")
        self.pwd = self.findChild(QtWidgets.QLineEdit, "inputPassword")

        self.ingreso.clicked.connect(self.click_ingreso)
        self.salida.clicked.connect(self.click_salir)

        # Inicializar la conexión a MongoDB aquí
        self.mongo_conn = MongoConnection()
        self.mongo_conn.connect()

    def click_salir(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Muchas Gracias por visitarnos!")
        msgBox.setWindowTitle("Salir del sistema")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            pass

    def click_ingreso(self):
        user = self.usr.text()
        password = self.pwd.text()

        validar = miLib.validaUsuario(user, password)
        if not validar:
            msgBox = QMessageBox()
            msgBox.setText("No tienes permiso para ingresar")
            msgBox.setWindowTitle("Sin Autorizacion")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
        else:
            self.abrir_ventana_principal()

    def abrir_ventana_principal(self):
        self.main_window = MainApp(self.mongo_conn) # Pasar la instancia de MongoConnection
        self.main_window.show()
        self.close()

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

