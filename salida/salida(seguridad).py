import time
import leerBotones as botones
import RPi.GPIO as GPIO
import leerConfiguracionFechaHora as confFH
import configuracionEXP as archivoConfiguracion
import fechaUTC

#import sys
#sys.path.append("../estacionamientoRed/cliente/")
import cliente as cliente

from threading import Thread
import sys
import os#commands, os
from escposprinter import *

GPIO.setmode(GPIO.BCM)

from PyQt4 import QtCore, QtGui

PATH_NOMBRE_PLAZA=str(archivoConfiguracion.getName())
DIRECCION_PLAZA=str(archivoConfiguracion.getDireccion())
terminalEnt=int(archivoConfiguracion.getNumTer())

activa=True

configuracion = []


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
		return QtGui.QApplication.translate(context, text, disambig)

class Ui_ventanaAcceso(object):
	def setupUi(self, ventanaAcceso):
		ventanaAcceso.setObjectName(_fromUtf8("ventanaAcceso"))
		ventanaAcceso.setEnabled(True)
		ventanaAcceso.resize(1366, 768)
		self.label = QtGui.QLabel(ventanaAcceso)
		self.label.setGeometry(QtCore.QRect(110, 20, 320, 91))
		font = QtGui.QFont()
		font.setPointSize(24)
		font.setBold(True)
		font.setWeight(75)
		self.label.setFont(font)
		self.label.setObjectName(_fromUtf8("label"))
		self.label_2 = QtGui.QLabel(ventanaAcceso)
		self.label_2.setGeometry(QtCore.QRect(0, 90, 481, 81))
		self.label_2.setObjectName(_fromUtf8("label_2"))
		self.label_3 = QtGui.QLabel(ventanaAcceso)
		self.label_3.setGeometry(QtCore.QRect(110, 150, 291, 101))
		self.label_3.setObjectName(_fromUtf8("label_3"))
		self.label_4 = QtGui.QLabel(ventanaAcceso)
		self.label_4.setGeometry(QtCore.QRect(60, 450, 391, 231))
		self.label_4.setObjectName(_fromUtf8("label_4"))
		self.Fecha = QtGui.QLabel(ventanaAcceso)
		self.Fecha.setGeometry(QtCore.QRect(10, 250, 500, 81))
		font = QtGui.QFont()
		font.setPointSize(16)
		font.setBold(True)
		font.setItalic(True)
		font.setWeight(75)
		self.Fecha.setFont(font)
		self.Fecha.setObjectName(_fromUtf8("Fecha"))
		self.Hora = QtGui.QLabel(ventanaAcceso)
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
	
	mensaje = 1
	f1 = f2 = f3 = f4 = f5 = f6 = False
	
	def leerBotones(self):
		
		tiempo = 0
		if self.mensaje == 1:
			self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\"></span></p></body></html>", None))
		elif self.mensaje == 2:
			self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Ingrese su boleto</span></p></body></html>", None))
		elif self.mensaje == 3:
			self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\"></span></p></body></html>", None))
		elif self.mensaje == 4:
			self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\"></span></p></body></html>", None))
		elif self.mensaje == 5:
			self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\"></span></p></body></html>", None))
		elif self.mensaje == 6:
			self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\"></span></p></body></html>", None))
		elif self.mensaje == 7:
			self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Sin coneccion a la Base de Datos</span></p></body></html>", None))
		if self.f1 != True:
			self.f2 = False
			print("------Preguntar Botones --------")
			if botones.leerMasa() == 1:
				if self.mensaje == 1:
					self.mensaje = 2
				if os.stat("datos.txt").st_size != 0:
					print("ticket detectado")
					self.f1 = True
					configuracion = []
					archivo=open("datos.txt", "r")
					contenido=archivo.readlines()
					i = 0
					for linea in contenido:
						configuracion.append(linea)
						if i == 0:
							idExp = linea
						if i == 1:
							idBol = linea
						if i == 2:
							fecBol = linea
						if i == 3:
							horBol = linea
						i+=1
					archivo.close()
					fechaConc=str(fecBol)+" "+str(horBol)
					print(idExp)
					print(idBol)
					print(fechaConc)
					archivo=open("datos.txt", "w")
					archivo.close()
					#pass
			elif botones.leerMasa() == 0:
				self.mensaje = 1
		if self.f1 == True and self.f2 == False:
				''' Operacion 1.- Autorizacion de salida'''
				#mensaje = (idBoleto,idExpedidora,fechaExpedicion)
				mensaje = idBol + "," + idExp + "," + fechaConc
				validacion = cliente.configSocket("autorizacion salida", mensaje)
				#validacion = "finalizado"
				print(validacion)
				if validacion == "finalizado":
					self.f2 = self.f3 = True
					self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Gracias por su visita</span></p></body></html>", None))
				elif validacion == "volver a pagar":
					self.f1 = False
					self.mensaje = 3
				elif validacion == "pago no realizado":
					self.f1 = False
					self.mensaje = 4
				elif validacion == "sin respuesta servidor":
					self.f1 = False
					self.mensaje = 5
				elif validacion == "sin comunicacion servidor":
					self.f1 = False
					self.mensaje = 6
				elif validacion == "error":
					self.f1 = False
					self.mensaje = 7
		if self.f1 == True and self.f2 == True:
			if self.f3 == True and self.f4 == False and self.f5 == False  and self.f6 == False:
				time.sleep(0.5)
				botones.abrir()
				while (self.f3 == True  and self.f4 == False):
					time.sleep(0.2)
					print ("Barrera Esperando que pase el carro...")
					self.f4 = botones.leerBobina2Subida()
				self.f3 = False
			if self.f3 == False and self.f4 == True and self.f5 == False and self.f6 == False:
				while (self.f4 == True and self.f5 == False):
					time.sleep(0.2)
					self.f5 = botones.abrirBarrera()
				self.f4 = False
			if self.f3 == False and self.f4 == False and self.f5 == True and self.f6 == False:
				while (self.f6 == False):
					time.sleep(0.2)
					self.f6 = botones.CerrarBarrera()
				self.f5 = False
			if self.f3 == False and self.f4 == False and self.f5 == False and self.f6 == True:
				botones.cerrar()
				print ("Ya cerre barrera restablesco fs")
				self.f1 = self.f2 = self.f3 = self.f4 = self.f5 = self.f6 = False
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

	def retranslateUi(self, ventanaAcceso):
		self.leerBotones()
		ventanaAcceso.setWindowTitle(_translate("ventanaAcceso", "ACCESO", None))
		self.label.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt;\"> Bienvenido </span></p></body></html>", None))
		self.label_2.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:22pt;\">"+PATH_NOMBRE_PLAZA+"</span></p></body></html>", None))
		self.mostrarFechayHora()
		
	def mensaje1(self):
		self.label_4.setText(_translate("ventanaAcceso", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Ingrese su boleto porfavor</span></p></body></html>", None))

def hilos():
	thread = Thread(target = activarFuncion, args=())
	thread1 = Thread(target = activarCamara, args=())
	try:
		thread.start()
		thread1.start()
	except Exception:
		pass
	print("chequeo")

def activarCamara():
	os.system("sudo zbarcam --raw  --prescale=50x50 >> datos.txt")

def activarFuncion():
	import sys
	app = QtGui.QApplication(sys.argv)
	ventanaAcceso = QtGui.QDialog()
	ui = Ui_ventanaAcceso()
	ui.setupUi(ventanaAcceso)
	ventanaAcceso.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	hilos()
	
