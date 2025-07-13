from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
import libreria_mongo as miLib

import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('login.ui', self) # Load the .ui file
        #self.resize(413, 243)
        self.adjustSize()

        self.show() # Show the GUI

        #ahora asocio los elementos del dibujo del designer al codigo python
        #y les doy nombres de atributos
        self.ingreso = self.findChild(QtWidgets.QPushButton, 'btnIngresar')
        self.salida = self.findChild(QtWidgets.QPushButton, 'btnSalir')

        self.usr = self.findChild(QtWidgets.QLineEdit, 'inputUsuario')
        self.pwd = self.findChild(QtWidgets.QLineEdit, 'inputPassword')

        #por ultimo a aquellos elementos que quiero
        #interactuen, les asocio un connect

        self.ingreso.clicked.connect(self.click_ingreso)
        self.salida.clicked.connect(self.click_salir)


    def click_salir(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText("Muchas Gracias por visitarnos!")
        msgBox.setWindowTitle("Salir del sistema")
        msgBox.setStandardButtons(QMessageBox.Ok)
        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print("OK")

    def click_ingreso(self):
        user=self.usr.text()
        password=self.pwd.text()

        print(user)
        print(password)

        validar=miLib.validaUsuario(user,password)
        if not validar:
            msgBox = QMessageBox()
            #msgBox.setIcon(QMessageBox.critical)
            msgBox.setText("No tienes permiso para ingresar")
            msgBox.setWindowTitle("Sin Autorizacion")
            msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = msgBox.exec()
        else:
            print("estamos listos!!")

    # def click_agregar(self):
    #     # This is executed when the button is pressed
    #     print('hizo click en el agregar')  
    #     print(self.nombre.text())      
    #     print(self.apellido.text())      


    # def click_editar(self):
    #     # This is executed when the button is pressed
    #     print('hizo click en el EDITAR')
    #     self.apellido.setText("Otro Apellido")

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
