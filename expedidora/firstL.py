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
from threading import Thread
from pygame import mixer
import psycopg2
import sys
import os
from escposprinter import *

GPIO.setmode(GPIO.BCM)

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox

limite_impresiones = 1600
boleto_previo = True
espera = 0
error_ayuda = 0	
estado = 0
plaza = ""
localidad = ""
terminalEnt = 0
usuario = 'postgres'
contrasenia = 'Postgres3UMd6'
bd = "dbeum_tecamac"

fechaIn	= fechaUTC.fechaConFormato()
horaEnt = fechaUTC.tiempoConFormato()

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

class Ui_ventanaAcceso(QDialog):

	def __init__(self):
		QDialog.__init__(self)
		gui = uic.loadUi("/home/pi/Documents/eum/app/expedidora/Interfaces_EXP/expedidora.ui", self)
		self.stackedWidget.setCurrentIndex(0)
		self.configurarPinesGPIO()
		self.datosEstacionamiento()
		self.pushButton.clicked.connect(lambda:self.reiniciarRasp())
		self.pushButton_3.clicked.connect(lambda:self.reiniciarRasp())
		self.pushButton_7.clicked.connect(lambda:self.reiniciarRasp())
		self.pushButton_2.clicked.connect(lambda:self.apagarRasp())
		self.pushButton_4.clicked.connect(lambda:self.apagarRasp())
		self.pushButton_8.clicked.connect(lambda:self.apagarRasp())
		self.pushButton_5.clicked.connect(lambda:self.reinicioConteo())
		self.pushButton_6.clicked.connect(lambda:self.reinicioConteo())
		self.pushButton_9.clicked.connect(lambda:self.reinicioConteo())
		self.pushButton_10.clicked.connect(lambda:self.impCabecera())
		self.pushButton_11.clicked.connect(lambda:self.impCabecera())
		self.pushButton_12.clicked.connect(lambda:self.impCabecera())
		self.leerBotones()
		#self.hilos2()

	def configurarPinesGPIO(self):
		botones.configurarPinesGPIO()
		botones.configurarPinesGPIOBobina()

	pantalla = 0
	inicio = 0
	error = 0
	antes = 0
	f1 = f2 = f3 = f4 = f5 = f6 = False
	def leerBotones(self):
		global boleto_previo, espera, limite_impresiones
		re.setReset()
		self.mostrarFechayHora()
		if self.pantalla == 0:
			self.stackedWidget.setCurrentIndex(0)
		elif self.pantalla == 1:
			if espera == 0:
				mixer.init()
				mixer.music.load('/home/pi/Documents/eum/app/expedidora/sonidos/mensaje2.mp3')
				mixer.music.play()
			self.stackedWidget.setCurrentIndex(1)
			espera = espera + 1
			if espera == 25:
				espera = 0
				self.pantalla = 0
		else:
			self.stackedWidget.setCurrentIndex(2)
			espera = espera + 1
			if espera == 25:
				espera = 0
				self.pantalla = 0
		if self.inicio == 0:
			self.error = 0
			self.inicio = 1
			self.checarFecha()
			self.limpiarBD()
			self.inicioImpresion()
			respuesta = imprimir.footer()
			self.finImpresion()
			if respuesta == "No esta conectada la impresora":
				mensaje = str(terminalEnt) + "," + str(4) + "," + str("iniciada")
				##########validacion = clientes.configSocket("log expedidora")
				##########clientes.logExpedidora(validacion,"log expedidora",mensaje)
				self.error = 3
				self.pantalla = 1
		if botones.leerAyuda() == 1:
			self.pantalla = 2
		if self.error == 0:
			if boleto_previo == True and self.f1 == False:
				self.inicioImpresion()
				respuesta = imprimir.imprimirHeader()
				self.finImpresion()
				if respuesta == "No esta conectada la impresora":
					mensaje = str(terminalEnt) + "," + str(4) + "," + str("iniciada")
					##########validacion = clientes.configSocket("log expedidora")
					##########clientes.logExpedidora(validacion,"log expedidora",mensaje)
					self.error = 3
					self.pantalla = 1
				else:
					boleto_previo = False
			else:
				if botones.leerMasa() == 1:
					if self.f1 == False:
						print("------Preguntar Botones --------")
						self.f1 = botones.leerBotonesEntrada()
					if self.f1 == True and self.f2 == False and self.f3 == False and self.f4 == False and self.f5 == False:
						if boleto_previo == False:
							noBolF = folio.saberFolio()
							folioBD = noBolF
							fechaIn	= fechaUTC.fechaConFormato()
							horaEnt = fechaUTC.tiempoConFormato()
							fechatimestamp = str(fechaIn)+" "+str(horaEnt)
							#self.insertarBoleto(plaza,terminalEnt,noBolF,fechatimestamp,'DEFAULT-ESCOM')
							''' Operacion 1.- Registro de boleto'''
							#mensaje = (idBoleto,idExpedidora,FechaExpedicion, idestado, idtipodescuento, idSalida)
							mensaje = noBolF + "," + str(terminalEnt) + "," + fechatimestamp + "," + str(1) + "," + str(1) + "," + str(0)
							##########validacion = clientes.configSocket("registro boleto")
							validacion="Modo local ON"
							if validacion == "error":
								self.f1 = self.f2 = self.f3 = self.f4 = self.f5 = False
								self.pantalla = 1
							else:
								##########valor = clientes.enviarMensaje(validacion,mensaje)
								valor=1
								if valor == "error":
									self.f1 = self.f2 = self.f3 = self.f4 = self.f5 = False
									self.pantalla = 1
								else:
									self.insertarBoleto(plaza,terminalEnt,noBolF,fechatimestamp,'DEFAULT-ESCOM')
									folio.escribirArchivoFolios(noBolF)
									self.inicioImpresion()
									print("aver si llego aqui")
									respuesta = imprimir.imprimirQR2(noBolF,str(terminalEnt),str(fechaIn),str(horaEnt))
									self.finImpresion()
									if respuesta == "No esta conectada la impresora":
										mensaje = str(terminalEnt) + "," + str(4) + "," + str("iniciada")
										##########validacion = clientes.configSocket("log expedidora")
										##########clientes.logExpedidora(validacion,"log expedidora",mensaje)
										self.error = 3
										self.pantalla = 1
									else:
										papel_cont = self.conteoBoletos()
										if papel_cont == limite_impresiones:
											#MANDAR MENSAJE AL SERVIDOR DE PAPEL CASI AGOTADO
											mensaje = str(terminalEnt) + "," + str(3) + "," + str("iniciada")
											##########validacion = clientes.configSocket("log expedidora")
											##########clientes.logExpedidora(validacion,"log expedidora",mensaje)
										papel_cont = papel_cont + 1
										self.aumentoConteo(papel_cont)
										mixer.init()
										mixer.music.load('/home/pi/Documents/eum/app/expedidora/sonidos/mensaje1.mp3')
										mixer.music.play()
										boleto_previo = True
										self.f2 = True
				if self.f2 == True and self.f3 == False and self.f4 == False  and self.f5 == False:
					if self.f6 == False:
						time.sleep(0.5)
						botones.abrir()
						self.f6 = True
					self.f3 = botones.leerBobina2Subida()
					if self.f3 == True:
						self.f2 = False
				if self.f2 == False and self.f3 == True and self.f5 == False:
					self.f4 = botones.abrirBarrera()
					if self.f4 == True:
						self.f3 = False
				if self.f2 == False and self.f3 == False and self.f4 == True:
					self.f5 = botones.CerrarBarrera()
					if self.f5 == True:
						self.f4 = False
				if self.f2 == False and self.f3 == False and self.f4 == False  and self.f5 == True:
					self.f1 = self.f2 = self.f3 = self.f4 = self.f5 = self.f6 = False
		elif self.error == 2:
			respuesta = imprimir.imprimirHeader()
			if respuesta == "ack":
				boleto_previo = False
				self.error = 0
		elif self.error == 3:
			respuesta = imprimir.instanciarImpresora()
			if respuesta != "No esta conectada la impresora":
				self.error = 0
		QtCore.QTimer.singleShot(200, self.leerBotones)

	def impCabecera(self):
		self.inicioImpresion()
		respuesta = imprimir.imprimirHeader()
		self.finImpresion()
		if respuesta == "No esta conectada la impresora":
			mensaje = str(terminalEnt) + "," + str(4) + "," + str("iniciada")
			##########validacion = clientes.configSocket("log expedidora")
			##########clientes.logExpedidora(validacion,"log expedidora",mensaje)
			self.error = 3
			self.pantalla = 1

	def inicioImpresion(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute(" UPDATE estado_impresora SET estado = 1,fecha = '"+ str(fechaUTC.fechaConFormato() + " " + fechaUTC.tiempoConFormato()) +"' WHERE idestadoimpresora = 1")
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def checarFecha(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute("SELECT max(fecha) FROM boletos;")
				row2 = cursor.fetchone()
				if row2[0] is not None:
					fec = row2[0].strftime("%d-%m-%Y")
					if fec != fechaUTC.fechaConFormato():
						escribeArch = open("/home/pi/Documents/eum/app/expedidora/archivos_config/UltimoFolio.txt","w")
						res = 0
						escribeArch.write(str(res)+"\n")
						escribeArch.close()
				else:
					escribeArch = open("/home/pi/Documents/eum/app/expedidora/archivos_config/UltimoFolio.txt","w")
					res = 0
					escribeArch.write(str(res)+"\n")
					escribeArch.close()	
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def limpiarBD(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				fecAct = fechaUTC.fechaConFormato()
				salto = 0
				dAct = ""
				mAct = ""
				aAct = ""
				for linea in fecAct:
					if salto == 0 and linea != "-":
						dAct = dAct + linea
					if salto == 1 and linea != "-":
						mAct = mAct + linea
					if salto == 2 and linea != "-":
						aAct = aAct + linea
					if linea == "-":
						salto = salto + 1
				mAct = int(mAct)
				aAct = int(aAct)
				if mAct > 4:
					mReg = mAct-4
					aReg = aAct
				else:
					mReg = 8 + mAct
					aReg = aReg - 1
				if mReg > 9:
					fechaReg = str(aReg) +"-"+str(mReg)+"-" + dAct +" 01:00:00"
				else:
					fechaReg = str(aReg) +"-0"+str(mReg)+"-" + dAct +" 01:00:00"
				cursor.execute("DELETE FROM boletos WHERE fecha < '{}';".format(fechaReg))
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def insertarBoleto(self,plz,terEnt,fol,fec,placa):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute("SELECT idplaza FROM plaza WHERE nombre_plaza = '" + plz + "';")
				row = cursor.fetchone()
				if row is not None:
					valor = int(row[0])
					connection.commit()
				cursor.execute("SELECT max(idboleto) FROM boletos;")
				row2 = cursor.fetchone()
				if row2[0] is not None:
					idbol = row2[0]
					idbol = idbol + 1
					connection.commit()
				else:
					idbol = 1
				cursor.execute("SELECT id_expedidora FROM datos_expedidora WHERE num_expedidora = {};".format(terEnt))
				row3 = cursor.fetchone()
				if row3[0] is not None:
					exp = row3[0]
					connection.commit()
				cursor.execute("INSERT INTO boletos (idboleto,plaza,expedidora,folio,fecha,placa) VALUES ({},{},{},{},'{}','{}');".format(idbol,valor,exp,fol,fec,placa))
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def finImpresion(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute(' UPDATE estado_impresora SET estado = 0 WHERE idestadoimpresora = 1')
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def mostrarFechayHora(self):
		fecha = fechaUTC.fechaConFormato()
		self.label_7.setText(fecha)
		self.label_9.setText(fecha)
		self.label_21.setText(fecha)
		hora = fechaUTC.tiempoConFormato()
		self.label.setText(hora)
		self.label_2.setText(hora)
		self.label_3.setText(hora)

	def apagarRasp(self):
		os.system("sudo shutdown -P 0")

	def reiniciarRasp(self):
		os.system("sudo shutdown -r 0")

	def datosEstacionamiento(self):
		self.nomPlaza_2.setText(plaza)
		self.nomPlaza_3.setText(plaza)
		self.nomPlaza_5.setText(plaza)
		self.nomLoc_2.setText(localidad)
		self.nomLoc_3.setText(localidad)
		self.nomLoc_5.setText(localidad)

	def conteoBoletos(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute(
					' SELECT conteo FROM contador_tickets WHERE idconteo = 1')
				row = cursor.fetchone()
				if row is not None:
					conteo = int(row[0])
					connection.commit()
					connection.close()
					return conteo
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def aumentoConteo(self,aumento):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute("UPDATE contador_tickets SET conteo = {} WHERE idconteo = 1".format(aumento))
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def reinicioConteo(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute("UPDATE contador_tickets SET conteo = 0 WHERE idconteo = 1")
				connection.commit()
				connection.close()
			self.impCabecera()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

class BotonAyuda():
	
	def __init__(self):
		self.configBotones()
		self.botonAyuda()
	
	def configBotones(self):
		botones.configurarPinesGPIO()
	
	
	def botonAyuda(self):
		global error_ayuda
		while (True):
			if botones.leerAyuda() == 1 and error_ayuda == 0:
				mixer.init()
				mixer.music.load('/home/pi/Documents/eum/app/expedidora/sonidos/mensajeayuda.mp3')
				mixer.music.play()
				mensaje = str(terminalEnt) + "," + str(1) + "," + str("iniciada")
				##########validacion = clientes.configSocket("log expedidora")
				##########clientes.logExpedidora(validacion,"log expedidora",mensaje)
				error_ayuda = 1
			if error_ayuda == 1 and botones.leerAyuda() == 0:
				error_ayuda = 0
			time.sleep(1)

class EstadoImpresion():

	def __init__(self):
		self.estadoImpresora()

	#estado 0 sin problemas, estado 1 iniciado, estado 2 error enviado
	def estadoImpresora(self):
		global estado
		while(True):
			estado = self.consultaEstadoImpresora()
			if estado == 1:
				tiempo = self.consultarTiempoImpresion()
				if tiempo > 6:
					mensaje = str(terminalEnt) + "," + str(2) + "," + str("iniciada")
					##########validacion = clientes.configSocket("log expedidora")
					##########clientes.logExpedidora(validacion,"log expedidora",mensaje)
					self.errorEnviado()
			time.sleep(.200)

	def errorEnviado(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute(' UPDATE estado_impresora SET estado = 2 WHERE idestadoimpresora = 1')
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def consultarTiempoImpresion(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute(
					' SELECT fecha FROM estado_impresora WHERE idestadoimpresora = 1')
				row = cursor.fetchone()
				if row is not None:
					tiempo = self.tiempoEspera(row[0].strftime("%Y-%m-%d %H:%M:%S"))
					connection.commit()
					connection.close()
					return tiempo
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

	def tiempoEspera(self,fecha_intento):
		tiempo_st = time.strptime(fecha_intento, "%Y-%m-%d %H:%M:%S")
		resultado = time.mktime(time.localtime()) - time.mktime(tiempo_st)
		return resultado

	def consultaEstadoImpresora(self):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute(
					' SELECT estado FROM estado_impresora WHERE idestadoimpresora = 1')
				row = cursor.fetchone()
				if row is not None:
					estado = int(row[0])
					connection.commit()
					connection.close()
					return estado
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)

def hilos():
	thread = Thread(target = activarFuncion, args=())
	thread1 = Thread(target = activarAyuda, args=())
	thread2 = Thread(target = activarEstadoImpresion, args=())
	try:
		thread.start()
		thread1.start()
		thread2.start()
	except Exception:
		pass

def obtenerPlazaYLocalidad():
	global plaza
	global localidad
	try:
		connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
		with connection.cursor() as cursor:
			cursor.execute(
				' SELECT nombre_plaza,estado FROM plaza WHERE idplaza = 1')
			row = cursor.fetchone()
			if row is not None:
				plaza = str(row[0])
				localidad = str(row[1])
				connection.commit()
				connection.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def obtenerTerminal():
	global terminalEnt
	try:
		connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
		with connection.cursor() as cursor:
			cursor.execute(
				' SELECT num_expedidora FROM datos_expedidora WHERE id_expedidora = 1')
			row = cursor.fetchone()
			if row is not None:
				terminalEnt = int(row[0])
				connection.commit()
				connection.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def activarEstadoImpresion():
	EstadoImpresion()

def activarAyuda():
	BotonAyuda()

def activarFuncion():
	import sys
	app = QApplication(sys.argv)
	ui = Ui_ventanaAcceso()
	ui.show()
	app.exec_()

if __name__ == "__main__":
	obtenerTerminal()
	obtenerPlazaYLocalidad()
	hilos()
