import time
import leerBotones as botones
import RPi.GPIO as GPIO
import leerConfiguracionFechaHora as confFH
import configuracionEXP as archivoConfiguracion
import fechaUTC
import os
import sys
import psycopg2
from pygame import mixer
import cliente as cliente
from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox
from threading import Thread
import sys
from escposprinter import *
from datetime import datetime, timedelta

GPIO.setmode(GPIO.BCM)
espera = 0
idSal = 0
reproduccion = 0
plaza = ""
localidad = ""
usuario = 'postgres'
contrasenia = 'Postgres3UMd6'
bd = "dbeum_tecamac"
rrr=0
red=59
green=109
blue=153
pantalla_cont = 0
iface=0
activa=True
camInicial=''
tolerancia=17
mensajeTolerancia=0

configuracion = []


fechaIn	=fechaUTC.fechaConFormato()
horaEnt=fechaUTC.tiempoConFormato()

horaDeApagado=confFH.getHora()

class Ui_ventanaAcceso(QDialog):

	global gui,iface

	def __init__(self):
		QDialog.__init__(self)
		iface=1
		gui = uic.loadUi("/home/pi/Documents/eum/app/salida/ventanas/rb.ui", self)
		self.stackedWidget.setCurrentIndex(0)
		self.configurarPinesGPIO()
		self.leerBotones()
		self.bapagar.clicked.connect(lambda:self.apagarRasp())
		self.breiniciar.clicked.connect(lambda:self.reiniciarRasp())
		self.bcamara.clicked.connect(lambda:self.cam())
		self.datosEstacionamiento()
		
		

	def configurarPinesGPIO(self):
		botones.configurarPinesGPIO()
		botones.configurarPinesGPIOBobina()

	mensaje = 0

	f1 = f2 = f3 = f4 = f5 = f6 = f7 = False
	error = 0

	def restar_hora(self,horab,fechab):
		global aux_dif
		"""formato = "%H:%M:%S"
		h1 = datetime.strptime(hora1, formato)
		h2 = datetime.strptime(hora2, formato)
		resultado = h1 - h2
		aux_dif=str(resultado)
		print("res:",h1,h2,resultado,type(str(resultado)))
		return str(resultado)"""
		fechaBoleto = datetime.strptime(str(fechab[0]) + str(fechab[1]) + str(fechab[2]), '%Y%m%d').date()
		horaBoleto = datetime.strptime(str(horab[0]) +':'+str(horab[1]) +':'+ str(horab[2]), '%H:%M:%S').time()
		fechaActual=datetime.now().date()
		horaActual=datetime.now().time()
		horayFechaBoleto = datetime.now().combine(fechaBoleto, horaBoleto)
		horayFechaActual = datetime.now().combine(fechaActual, horaActual)
		restaFechas = horayFechaActual - horayFechaBoleto
		aux_dif=str(restaFechas)
		dias = int(restaFechas.days)
		horas = int(restaFechas.seconds / 3600)
		minutos= int(restaFechas.seconds / 60)
		return dias,horas,minutos


	def leerBotones(self):
		global espera,pantalla_cont,reproduccion,red,green,blue,rrr,iface
		
		if(red<50):
			rrr=1
		if(red>150):
			rrr=0
		if(rrr==0):
			red=red-20
			green=green-20
			blue=blue-20
		else:
			red=red+20
			green=green+20
			blue=blue+20
			
		self.lboleto.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");background-color:transparent;")
		
		self.fechaLabel()
		tiempo = 0
		if self.f1 != True:
			self.f2 = False
			print("------Preguntar Botones --------")
			if(iface==1):
				iface=0
				self.apagarRasp()
			#self.apagarRasp()
			if pantalla_cont > 0:
				pantalla_cont = pantalla_cont + 1
				print(pantalla_cont)
				if pantalla_cont == 30:
					self.stackedWidget.setCurrentIndex(0)
					self.lboleto.setText("---> Inserte su boleto <---")
					pantalla_cont = 0
			if botones.leerMasa() == 1:
				if self.error == 0 and botones.leerAyuda() == 1:
					#Agregar dato desde la BD
					mensaje_envio = str(idSal) + "," + str(1) + "," + str("iniciado") + ","
					validacion = cliente.configSocket("log salida", mensaje_envio)
					self.error = 1
					mixer.init()
					mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensajeayuda.mp3')
					mixer.music.play()
					#self.stackedWidget.setCurrentIndex(8)
					print("dentro del error")
				elif self.error == 1 and botones.leerAyuda() == 0:
					print("dentro del contador:")
					print(espera)
					espera = espera + 1
					if espera == 25:
						espera = 0
						self.error = 0
						#self.stackedWidget.setCurrentIndex(1)
				elif self.error == 0 and botones.leerAyuda() == 0:
					if self.mensaje == 1:
						archivo = open("datos.txt", "w")
						archivo.close()
						self.mensaje = 0
						#self.stackedWidget.setCurrentIndex(1)
						mixer.init()
						mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje1.mp3')
						mixer.music.play()
					if os.stat("datos.txt").st_size != 0:
						archivo = open("datos.txt", "r")
						contenido = archivo.readlines()
						banner2 = False
						#IF para validar que el boleto se pudo leer de manera correcta
						for linea in contenido:
							if linea == "Estacionamientos unicos de Mexico\n":
									banner2 = True
						archivo.close()
						if banner2 == True:
							os.system("sudo wmctrl -a 'zbar'")
							print("ticket detectado")
							self.f1 = True
							archivo = open("datos.txt", "r")
							contenido = archivo.readlines()
							i = 0
							banner = False
							tam = len(contenido)
							for linea in contenido:
								if i == 1:
									idBol = linea
								if i == 2:
									idExp = linea
								if i == 3:
									fecBol = linea
								if i == 4:
									horBol = linea
								if linea == "Estacionamientos unicos de Mexico\n":
									banner = True
								if banner == True:
									i+=1
							archivo.close()
							aux = ""
							i = 0
							idExp = int(idExp)
							idBol = int(idBol)
							for dat in fecBol:
								if i < 10:
									aux = aux + dat
								i += 1
							fecBol = aux
							aux = ""
							i = 0
							for dat in horBol:
								if i < 8:
									aux = aux + dat
								i += 1
							horBol = aux
							i = 0
							aux = ""
							for dat in fecBol:
								if i > 5:
									aux = aux + dat
								i += 1
							aux = aux + "-"
							i = 0
							for dat in fecBol:
								if i > 2 and i < 5:
									aux = aux + dat
								i += 1
							aux = aux + "-"
							i = 0
							for dat in fecBol:
								if i < 2:
									aux = aux + dat
								i += 1
							fecBol = aux
							print(str(idExp) + " " + str(idBol) + " " + fecBol + " " + horBol)
							fechaConc = str(fecBol)+ " " + str(horBol)
							#archivo = open("datos.txt", "w")
							#archivo.close()
							#pass

						else:
							self.mensaje = 9
			elif botones.leerMasa() == 0:
				self.mensaje = 1
				self.stackedWidget.setCurrentIndex(0)
		if self.f1 == True and self.f2 == False:
				''' Operacion 1.- Autorizacion de salida'''
				mensaje_envio = str(idBol) + "," + str(idExp) + "," + fechaConc + "," + str(1)
				validacion = cliente.configSocket("autorizacion salida", mensaje_envio)



				leerArch = open("datos.txt", "r")
				leyenda=(leerArch.readline().rstrip("\n")).lstrip("\x00")
				folio=(leerArch.readline().rstrip("\n")).lstrip("\x00")
				inTerminal=leerArch.readline().rstrip("\n")
				inFecha=leerArch.readline().rstrip("\n")
				inHora=leerArch.readline().rstrip("\n")
				readQR = []
				readQR.append(folio)
				readQR.append(inTerminal)
				readQR.append(inFecha)
				readQR.append(inHora)

				print(readQR,"len=",readQR.__len__())
				fo=readQR[0]
				pe=readQR[1]
				hh=readQR[3]
				#hsalida=fechaUTC.mostrarHoraSinFormato()[0]+":"+fechaUTC.mostrarHoraSinFormato()[1]+":"+fechaUTC.mostrarHoraSinFormato()[2]
				h= readQR[3].rstrip("\n")
				fe = readQR[2].rstrip("\n")



				leerArch.close()
				leerArch = open("datos.txt", "w")
				leerArch.write('')
				leerArch.close()
				print("FEEEE>>>>>",fo)



				horaBoleto=h.split(':',2)
				fechaAMD=fe.split('-',2)
				#fechaAMD=fe
				print("fechas----->",fe,fechaAMD)
				fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]


				dh=self.restar_hora(horaBoleto,fechaAMD.split('-'))

				dias=dh[0]
				horas=dh[1]
				minutos=dh[2]
				horas=horas+(dias*24)
				tiempoEstacionado=horas
				print("DHDHDHDHDHDHDHDHDHD",dh)
				print("DHDHDHDHDHDHDHDHDHD",dh)
				print("DHDHDHDHDHDHDHDHDHD",dh)
				if(dias==0):
					if(minutos<tolerancia):
						validacion="finalizado"
						botones.abrir()
						print("abrido")


				print(validacion)
				#self.lboleto.setText(validacion)
				if validacion == "finalizado":
					self.f2 = self.f3 = True
				elif validacion == "volver a pagar":
					self.lboleto.setText("---> 	Tiempo de salida excedido <---")
					mixer.init()
					mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje4.mp3')
					mixer.music.play()
					self.f1 = False
					#self.stackedWidget.setCurrentIndex(4)
					pantalla_cont = 1
				elif validacion == "pago no realizado":
					self.lboleto.setText("---> Favor de pagar su boleto... <---")
					mixer.init()
					mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje2.mp3')
					mixer.music.play()
					self.f1 = False
					#self.stackedWidget.setCurrentIndex(2)
					pantalla_cont = 1
				elif validacion == "boleto no encontrado":
					mixer.init()
					self.lboleto.setText("---> Favor de pagar su boleto <---")
					mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje2.mp3')
					#mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje7.mp3')
					mixer.music.play()
					self.f1 = False
					#self.stackedWidget.setCurrentIndex(7)
					pantalla_cont = 1
				elif validacion == "boleto obsoleto":
					self.lboleto.setText("---> Boleto usado <---")
					mixer.init()
					mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje3.mp3')
					mixer.music.play()
					self.f1 = False
					#self.stackedWidget.setCurrentIndex(3)
					pantalla_cont = 1
				elif validacion == "sin comunicacion servidor":
					mixer.init()
					mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje5.mp3')
					mixer.music.play()
					self.f1 = False
					#self.stackedWidget.setCurrentIndex(5)
					pantalla_cont = 1
				elif validacion == "error":
					mixer.init()
					mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje5.mp3')
					mixer.music.play()
					self.f1 = False
					#self.stackedWidget.setCurrentIndex(5)
					pantalla_cont = 1
		if self.f1 == True and self.f2 == True:
			#self.stackedWidget.setCurrentIndex(6)
			pantalla_cont = 1
			if reproduccion == 0:
				self.lboleto.setText("---> Retire su boleto <---")
				mixer.init()
				mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensajeboleto.mp3')
				mixer.music.play()
				time.sleep(3.2)
				mixer.music.load('/home/pi/Documents/eum/app/salida/sonidos/mensaje6.mp3')
				mixer.music.play()
				reproduccion = 1
			if self.f3 == True and self.f4 == False and self.f5 == False  and self.f6 == False:
				if self.f7 == False:
					time.sleep(0.5)
					botones.abrir()
					self.f7 = True
				self.f4 = botones.leerBobina2Subida()
				if self.f4 == True:
					self.f3 = False
			if self.f3 == False and self.f4 == True and self.f5 == False and self.f6 == False:
				self.f5 = botones.abrirBarrera()
				if self.f5 == True:
					self.f4 = False
			if self.f3 == False and self.f4 == False and self.f5 == True and self.f6 == False:
				self.f6 = botones.CerrarBarrera()
				if self.f6 == True:
					self.f5 = False
			if self.f3 == False and self.f4 == False and self.f5 == False and self.f6 == True:
				print ("Ya cerre barrera restablesco fs")
				self.f1 = self.f2 = self.f3 = self.f4 = self.f5 = self.f6 = self.f7 = False
				reproduccion = 0
		QtCore.QTimer.singleShot(100, self.leerBotones)

	def fechaLabel(self):
		fecha = fechaUTC.fechaConFormato()
		self.ldate2.setText(fecha)
		
		hora = fechaUTC.tiempoConFormato()
		self.ltime2.setText(hora)


	def datosEstacionamiento(self):
		#self.nomPlaza_2.setText(plaza)
		#self.nomLoc_2.setText(localidad)
		self.nomPlaza_2.setText(" WALMART")
		self.nomLoc_2.setText(" JIUTEPEC")

	def cam(self):
		print("reiniciando...")
		thread1 = Thread(target = activarCamara, args=())
		try:
			a=thread1.start()
			print("hiulo1",a)
		except Exception:
			pass
		#os.system("sudo wmctrl -r 'zbar' -e 0,950,780,250,170")
		
		#os.system("sudo wmctrl -r 'Dialog' -e 0,0,-30,1900,1050")
		#os.system("sudo wmctrl -a 'zbar'")
		
		#os.system("sudo shutdown -P 0")

	def reiniciarRasp(self):
		os.system("sudo shutdown -r 0")
	def apagarRasp(self):
		os.system("sudo shutdown 0")

def obtenerPlazaYLocalidad():
	global plaza, localidad
	try:
		connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
		with connection.cursor() as cursor:
			cursor.execute(
				' SELECT nombre_plaza,estado FROM plaza WHERE idplaza = 1')
			row = cursor.fetchone()
			if row is not None:
				print("columns: {}, {}".format(row[0], row[1]))
				plaza = str(row[0])
				localidad = str(row[1])
				connection.commit()
				connection.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def obtenerIdSal():
	global idSal
	try:
		connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
		with connection.cursor() as cursor:
			cursor.execute(
				' SELECT num_salida FROM datos_salida WHERE id_salida = 1')
			row = cursor.fetchone()
			if row is not None:
				print("columns: {}".format(row[0]))
				idSal = int(row[0])
				connection.commit()
				connection.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

def hilos():
	thread = Thread(target = activarFuncion, args=())
	thread1 = Thread(target = leerCodQR, args=())
	thread4 = Thread(target=buscaCamara, args=())

	try:
		thread.start()
		thread4.start()
		thread1.start()
	except Exception:
		pass
def buscaCamara():
	global camInicial
	while(1):
		lee2 = os.system("sudo find /dev -name 'video*' > cam.txt")
		a = open("cam.txt", "r")
		cam=(a.readline().rstrip("\n")).lstrip("\x00")
		a.close()
		a = open("cam.txt", "w")
		a.write('')
		time.sleep(1)
		print('Cammmmmmmmm',cam,camInicial)
		if(cam!=camInicial):
			print('Camara desconectadaaaaaaaaa')
			os.system("sudo pkill zbarcam")
			
def leerCodQR():
	global camInicial
	time.sleep(1)
	lee2 = os.system("sudo find /dev -name 'video*' > cam.txt")
	a = open("cam.txt", "r")
	cam=(a.readline().rstrip("\n")).lstrip("\x00")
	a.close()
	a = open("cam.txt", "w")
	a.write('')
	camInicial=cam
	print('CamInicial',camInicial)
	while(1):
		time.sleep(1)
		lee2 = os.system("sudo find /dev -name 'video*' > cam.txt")
		a = open("cam.txt", "r")
		cam=(a.readline().rstrip("\n")).lstrip("\x00")
		a.close()
		a = open("cam.txt", "w")
		a.write('')
		print('Cam',cam,camInicial)
		if(cam==camInicial):

			try:
				print('Camara Detectada')
				lee = os.system("sudo zbarcam --raw  --prescale=280x150  "+cam+"  >> datos.txt")
				#lee = os.system("zbarcam --raw  --prescale=10x10 /dev/video0 > /home/pi/Documents/eum/app/caseta/ticket.txt")
				#lee = os.system("/home/pi/Documents/eum/app/caseta/dsreader -l 27 -b 14 -r 30 -s 100 -u 50  > /home/pi/Documents/eum/app/caseta/ticket.txt")
				#lee = os.system("cd /home/pi/scanner/dsreader")
				#lee = os.system("./dsreader -l 27 -b 14 -r 30 -s 100 -u 50  > /home/pi/Documents/eum/app/caseta/ticket.txt")

			except e:
				mensajeTolerancia=1
				print("Error al crear el socket: ",e)
		else:
			
			if(cam!=''):
				camInicial=cam
			else:
				print('Camara desconectada')


def activarCamara():
	#os.system("sudo zbarcam --raw  --prescale=50x50 >> datos.txt")
	os.system("sudo zbarcam --raw  --prescale=280x150 >> datos.txt")
	

def activarFuncion():
	import sys
	app = QApplication(sys.argv)
	ui = Ui_ventanaAcceso()
	ui.show()
	app.exec_()

if __name__ == "__main__":
	hilos()
	obtenerIdSal()
	obtenerPlazaYLocalidad()
	time.sleep(3)
	#os.system("sudo wmctrl -r 'Dialog' -e 0,0,430,1900,50")

	
	
