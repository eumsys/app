# -*- coding: utf-8 -*-

#CONTROLADOR
import time
import leerBotones as botones
import generarFolio as folio
import codigoQR as qr
import imprimirBoleto as imprimir
import tratarImagen as imagen
import fechaUTC
import RPi.GPIO as GPIO
import configuracionEXP as archivoConfiguracion
import cortesExpFun as conectionBD
import resetFolios as re
import leerConfiguracionFechaHora as confFH
import cliente as clientes

import sys
import os#commands, os
from escposprinter import *

 
GPIO.setmode(GPIO.BCM)

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox

PATH_NOMBRE_PLAZA=str(archivoConfiguracion.getName())
DIRECCION_PLAZA=str(archivoConfiguracion.getDireccion())
terminalEnt=int(archivoConfiguracion.getNumTer())

boleto_previo=True

fechaIn	=fechaUTC.fechaConFormato()
horaEnt=fechaUTC.tiempoConFormato()

horaDeApagado=confFH.getHora()


try:
	_fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
	def _fromUtf8(s):
		return s

try:
	_encoding = QtGui.QApplication.UnicodeUTF8
	def _translate(context, text, disambig):
		return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
	def _translate(context, text, disambig):
		return QApplication.translate(context, text, disambig)

class Ui_ventanaAcceso(object):
	def setupUi(self, ventanaAcceso):
		ventanaAcceso.setObjectName(_fromUtf8("ventanaAcceso"))
		ventanaAcceso.setEnabled(True)
		ventanaAcceso.resize(1366, 768)
		self.label = QLabel(ventanaAcceso)
		self.label.setGeometry(QtCore.QRect(110, 20, 320, 91))
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QLabel(ventanaAcceso)
		self.label_2.setGeometry(QtCore.QRect(0, 90, 481, 81))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QLabel(ventanaAcceso)
		self.label_3.setGeometry(QtCore.QRect(110, 150, 291, 101))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QLabel(ventanaAcceso)
		self.label_4.setGeometry(QtCore.QRect(60, 450, 391, 231))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.Fecha = QLabel(ventanaAcceso)
		self.Fecha.setGeometry(QtCore.QRect(10, 250, 500, 81))
		font = QtGui.QFont()
		font.setPointSize(16)
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		self.Fecha.setFont(font)
		self.Fecha.setObjectName(_fromUtf8("Fecha"))
		self.Hora = QLabel(ventanaAcceso)
		self.Hora.setGeometry(QtCore.QRect(60, 390, 431, 91))
		font = QtGui.QFont()
		font.setPointSize(16)
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		self.Hora.setFont(font)
		self.Hora.setObjectName(_fromUtf8("Hora"))
		
		self.configurarPinesGPIO()
		self.retranslateUi(ventanaAcceso)
		self.leerBotones()
		QtCore.QMetaObject.connectSlotsByName(ventanaAcceso)

	def configurarPinesGPIO(self):
		botones.configurarPinesGPIO()
		botones.configurarPinesGPIOBobina()
		
	def leerBotones(self):
		global boleto_previo
		re.setReset()
		print("------Preguntar Botones --------")
		f2 = f3 = f4 = f5 = False
		f1 = botones.leerBotonesEntrada() #f6=botones.leerBobina2Subida() #PREGUNTAR POR LA BOBINA EN EL PIN CORRECTO
		if boleto_previo == True:	#Imprimir cabecera()
			print ("Imprimo la cabecera para tener listo el boleto...")
			imprimir.imprimirHeaderHermosillo()
			boleto_previo = False
		else:  
			if f1 == True and f2 == False and f3 == False and f4 == False and f5 == False:
				noBolF = folio.saberFolio()
				folioBD = noBolF
				print ("Folio:" + noBolF)
				#noBol=noBolF.replace('GM:', '')
				fechaIn	= fechaUTC.fechaConFormato()
				horaEnt = fechaUTC.tiempoConFormato()
				print ("Bandera f2=True se termino de imprimir") 
				print ("Se agrega Boleto a la base de datos de la expedidora")
				fechatimestamp = str(fechaIn)+" "+str(horaEnt)
				conectionBD.insertarBoleto(PATH_NOMBRE_PLAZA,terminalEnt,str(folioBD),fechatimestamp,'DEFAULT-ESCOM')
				
				
				''' Operacion 1.- Registro de boleto'''
				#mensaje = (idBoleto,idExpedidora,FechaExpedicion, idestado, idtipodescuento, idSalida)
				mensaje = noBolF + "," + str(terminalEnt) + "," + fechatimestamp + "," + str(1) + "," + str(0) + "," + str(0)
				
				validacion = clientes.configSocket("registro boleto")
				
				#print(validacion)
				if validacion == "error":
					print("error de conexion")
					f1 = f2 = f3 = f4 = f5 = False
				else:
					imprimir.imprimirQR2(noBolF,str(terminalEnt),str(fechaIn),str(horaEnt))
					boleto_previo = True #Se completa la primera face y se puede volver a imprimir unas cabecera.
					f2 = True
					clientes.enviarMensaje(validacion,mensaje)
				
				
			if f2==True and f3==False and f4==False  and f5==False:
				time.sleep(0.5)
				botones.abrir()
				while (f2==True  and f3==False):
					time.sleep(0.2)
					print ("Barrera Esperando que pase el carro...")
					f3=botones.leerBobina2Subida()
				f2=False
			if f2==False and f3==True and f4==False  and f5==False:
				while (f3==True  and f4==False):
					time.sleep(0.2)
					f4=botones.abrirBarrera()
				f3=False
			if f2==False and f3==False and f4==True  and f5==False:
				while (f5 == False):
					time.sleep(0.2)
					f5=botones.CerrarBarrera()
				f4=False
			if f2==False and f3==False and f4==False  and f5==True:
				print ("Ya cerre barrera restablesco fs")
				f1=f2=f3=f4=f5=False
		QtCore.QTimer.singleShot(200, self.leerBotones)

	def mostrarFechayHora(self):
		F=time.strftime("%d / %B / %Y")
		H=time.strftime("%H:%M:%S")
		self.apagarExp(H)
		self.Fecha.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:25pt;\">"+F+ "</span></p></body></html>", None))
		self.Hora.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:48pt;\">"+H+"</span></p></body></html>", None))
		QtCore.QTimer.singleShot(1000, self.mostrarFechayHora)

	def apagarExp(self,H):
		if horaDeApagado==H:
			print ("Se apaga el sistema" )
			os.system("sudo shutdown 0")
		#if botones.botonApagarGPIO()==True:
		#	print "Se apaga el sistema" 
		#	os.system("sudo shutdown 0")

	def retranslateUi(self, ventanaAcceso):
		self.leerBotones()
		ventanaAcceso.setWindowTitle(_translate("ventanaAcceso", "ACCESO", None))
		self.label.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt;\">Bienvenido </span></p></body></html>", None))
		self.label_2.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt;\">"+PATH_NOMBRE_PLAZA+"</span></p></body></html>", None))
		self.mostrarFechayHora()
		self.label_3.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">("+DIRECCION_PLAZA+")</span></p></body></html>", None))
		self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:21pt; font-weight:600; font-style:italic;\">Es un placer atenderle:</span></p><p align=\"center\"><span style=\" font-size:20pt; font-weight:600; font-style:italic;\">Obtenga su ticket <br/> presionando el botón</span></p></body></html>", None))

if __name__ == "__main__":
	import sys
	#app = QtGui.QApplication(sys.argv)
	app = QApplication(sys.argv)
	ventanaAcceso = QDialog()
	ui = Ui_ventanaAcceso()
	ui.setupUi(ventanaAcceso)
	ventanaAcceso.show()
	sys.exit(app.exec_())
