from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QApplication
from mongo_connection import MongoConnection
import sys

class LoginApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(LoginApp, self).__init__()
        uic.loadUi('login.ui', self)
        self.adjustSize()
        
        # Inicializar conexión a MongoDB
        self.mongo_conn = MongoConnection()
        
        # Conectar elementos de la interfaz
        self.ingreso = self.findChild(QtWidgets.QPushButton, 'btnIngresar')
        self.salida = self.findChild(QtWidgets.QPushButton, 'btnSalir')
        self.usr = self.findChild(QtWidgets.QLineEdit, 'inputUsuario')
        self.pwd = self.findChild(QtWidgets.QLineEdit, 'inputPassword')
        
        # Conectar eventos
        self.ingreso.clicked.connect(self.click_ingreso)
        self.salida.clicked.connect(self.click_salir)
        
        # Conectar a MongoDB al inicializar
        if not self.mongo_conn.connect():
            self.mostrar_mensaje("Error", "No se pudo conectar a la base de datos MongoDB", QMessageBox.Critical)
        
        self.show()
    
    def click_salir(self):
        """
        Maneja el evento de salir de la aplicación
        """
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("¡Muchas gracias por usar ComercioTech!")
        msgBox.setWindowTitle("Salir del sistema")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.mongo_conn.disconnect()
            self.close()
    
    def click_ingreso(self):
        """
        Maneja el evento de ingreso al sistema
        """
        usuario = self.usr.text().strip()
        password = self.pwd.text().strip()
        
        if not usuario or not password:
            self.mostrar_mensaje("Error", "Por favor ingrese usuario y contraseña", QMessageBox.Warning)
            return
        
        # Validar credenciales
        if self.mongo_conn.validar_usuario(usuario, password):
            self.mostrar_mensaje("Éxito", "¡Bienvenido al sistema ComercioTech!", QMessageBox.Information)
            # Aquí se abriría la ventana principal
            self.abrir_ventana_principal()
        else:
            self.mostrar_mensaje("Error", "Usuario o contraseña incorrectos", QMessageBox.Critical)
    
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
    
    def abrir_ventana_principal(self):
        """
        Abre la ventana principal de la aplicación
        """
        from main_app import MainApp
        self.main_window = MainApp(self.mongo_conn)
        self.main_window.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    sys.exit(app.exec_())

