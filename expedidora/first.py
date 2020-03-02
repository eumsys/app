#!/usr/bin/env python3
import time
import leerBotones as botones
import generarFolio as folio
#import codigoQR as qr
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
from PIL import Image, ImageDraw, ImageFont


GPIO.setmode(GPIO.BCM)

from PyQt5 import QtCore, QtGui, uic
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox


limite_impresiones = 1000
boleto_previo = True
espera = 0
error_ayuda = 0	
estado = 0
usuario = 'postgres'
contrasenia = 'Postgres3UMd6'
bd = "dbeum_tecamac"
rrr=0
red=59
green=109
blue=153
fechaIn	= fechaUTC.fechaConFormato()
horaEnt = fechaUTC.tiempoConFormato()
cont=0
USUARIO=''
host=''
ip=''
noEquipo = 0
plaza = ""
localidad = ""
conn = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
cur=conn.cursor()

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
		
		self.breiniciar.clicked.connect(lambda:self.reiniciarRasp())
		self.bapagar.clicked.connect(lambda:self.apagarRasp())
		self.pushButton_3.clicked.connect(lambda:self.reiniciarRasp())
		self.pushButton_4.clicked.connect(lambda:self.apagarRasp())
		self.pushButton_5.clicked.connect(lambda:self.reinicioConteo())
		self.pushButton_6.clicked.connect(lambda:self.reinicioConteo())

		
		
		self.leerBotones()
		
		###MODULOSSSSSSSS############
		self.bconfirmarIP.clicked.connect(self.cambiaIp)
		self.bpanelconf.clicked.connect(self.muestraPanel)
		self.bsalirConfig.clicked.connect(lambda:self.cambia(0))
		self.bsalirLogin.clicked.connect(lambda:self.cambia(0))
		self.bsalirsucursal.clicked.connect(lambda:self.cambia(4))
		self.bsalirred.clicked.connect(lambda:self.cambia(4))
		self.bsalirCambiarFecha.clicked.connect(lambda:self.cambia(4))
		self.bsucursal.clicked.connect(lambda:self.cambia(3))
		self.bred.clicked.connect(lambda:self.cambia(2))
		self.breporte.clicked.connect(lambda:self.cambia(0))
		self.bhora.clicked.connect(lambda:self.cambia(6))
		
		self.lerror1.setVisible(False)
		self.bentrar.clicked.connect(self.validaLogin)
		self.bcambiarFecha.clicked.connect(self.cambiaFecha)
		#self.bguardar.clicked.connect(self.setConfig)
		#self.bsalirConfig.clicked.connect(self.salirConf)
		self.bconfirmarplaza.clicked.connect(self.setConfig)
		self.panelConfig()
		self.datosEstacionamiento()

	def validaLogin(self):
		global cur,accesoAcaja,USUARIO,correoUSUARIO
		nom=self.lusu.text()
		rol_us=""
		indice=0
		contr=self.lcont.text()
		if(nom == "eum" and contr == "pi"):
			self.cambia(5)
		else:
			self.lerror1.setText("usuario o contraseña incorrectos")
			self.lerror1.setVisible(True)
			
	
	def cambiaFecha(self):
		a=self.dtime.dateTime()
		b=self.dtime.textFromDateTime(a)
		print(b,type(b))
		os.system("sudo date -s '"+b+"' ")
		
	def setConfig(self):
		global plaza,localidad,noEquipo,host,ip,pol,pol1,pol2,pol3,pol4,pol5,impresora,anchoPapel
		lenn=0
		plaza=str(self.lnom.text())
		localidad=str(self.lloc.text())
		noEquipo=str(self.leq.text())
		
		
		print(plaza,localidad)
		dat=plaza+","+localidad+","+str(noEquipo)
		infile = open("/home/pi/Documents/eum/app/expedidora/archivos_config/datos.txt", 'w')
		c=infile.write(dat)
		
		self.datosEstacionamiento()
		self.cambia(0)
		
	
		
		
		
		
	def datosEstacionamiento(self):
		global plaza,localidad,noEquipo,host,ip,pol,pol1,pol2,pol3,pol4,pol5,impresora,anchoPapel
		lenn=0
		self.lnom.setText(plaza)
		self.lloc.setText(localidad)
		self.leq.setText(str(noEquipo))
		self.nomPlaza.setText(plaza)
		self.nomLoc.setText(localidad)
		self.lhost.setText(host)
		self.lip.setText(ip)
		
		
	def panelConfig(self):
		global plaza,localidad,noEquipo,host,ip
		infile = open('/home/pi/Documents/eum/app/expedidora/archivos_config/datos.txt','r')
		datos= infile.readline()
		arr=datos.split(',')
		plaza=arr[0]
		localidad=arr[1]
		noEquipo=arr[2]
		infile.close()
		
		infile = open('/home/pi/Documents/eum/app/expedidora/archivos_config/red.txt','r')
		datos= infile.readline()
		arr=datos.split(',')
		host=arr[0]
		ip=arr[1]
		infile.close()
		
		
	def salirConf(self):
		global panelConf
		panelConf=0
		self.cambia(1)
		

	
	
	
	def sustituye(self,archivo,buscar,reemplazar):
		"""

		Esta simple función cambia una linea entera de un archivo

		Tiene que recibir el nombre del archivo, la cadena de la linea entera a

		buscar, y la cadena a reemplazar si la linea coincide con buscar

		"""
		with open(archivo, "r") as f:

			# obtenemos las lineas del archivo en una lista

			lines = (line.rstrip() for line in f)
			print(lines)

	 

			# busca en cada linea si existe la cadena a buscar, y si la encuentra

			# la reemplaza

			

			altered_lines = [reemplazar if line==buscar else line for line in lines]
			f= open(archivo, "w+")
			print(altered_lines[0],len(altered_lines))
			for i in range(len(altered_lines)):
				if(buscar in altered_lines[i]):
					print (altered_lines[i])
					cambia=altered_lines[i]
					f.write(reemplazar+"\n")
				else:
					f.write(altered_lines[i]+"\n")
			f.close()
			
			
	def setPlazaYLocalidad(self,plaza,localidad):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				print("mmm",plaza,localidad)
				cursor.execute(" UPDATE plaza set nombre_plaza = '"+str(plaza)+"' WHERE idplaza = 1")

				
				cursor.execute(" UPDATE plaza set estado = '"+str(localidad)+"' WHERE idplaza = 1")
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)



	def setTerminal(self,noEquipo):
		try:
			connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
			with connection.cursor() as cursor:
				cursor.execute(" UPDATE datos_expedidora set num_expedidora ="+str(noEquipo)+" WHERE id_expedidora = 1")
				connection.commit()
				connection.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print(error)
		
	def cambia(self,val):
		self.stackedWidget.setCurrentIndex(val)
		
	def muestraPanel(self):
		self.cambia(4)
		#datos=obtenerPlazaYLocalidad()
		#self.lno.setText(str(datos[0]))
		#self.llo.setText(str(datos[1]))
		#datos=obtenerTerminal()
		self.lusu.setText('')
		self.lcont.setText('')
		self.lerror1.setText('')
	def cambiaNombre(self,val):
		plaza=str(self.lno.text())
		loc=str(self.llo.text())
		noEquipo=str(self.le.text())
		print(plaza,loc)
		datos=self.setPlazaYLocalidad(plaza,loc)
		
		datos=self.setTerminal(noEquipo)
		if(self.ch1.checkState()==2):
			print("ESTACHECK")
		else:
			self.sustituye("/etc/profile","sudo python3 /home/pi/Documents/eum/app/expedidora/first.py","sudo python3 /home/pi/Documents/eumL/app/expedidora/first.py")
	def cambiaI2P(self,val):
		host=self.lhost.text()
		ip=self.lip.text()
		
		self.sustituye("/home/pi/Documents/eum/app/expedidora/cliente.py","192.168","host = '"+host+"'")
		self.sustituye("/etc/dhcpcd.conf","ip_address","static ip_address="+ip+"/24")
		ip=ip.split(".")
		ip=ip[0]+"."+ip[1]+"."+ip[2]+".1"
		self.sustituye("/etc/dhcpcd.conf","routers","static routers="+ip)
		
	def cambiaIp(self):
		global host,ip
		host=self.lhost.text()
		ip=self.lip.text()

		self.sustituye("/home/pi/Documents/eum/app/cajeroF/cajero/cliente.py","192.168","host = '"+host+"'")
		self.sustituye("/etc/dhcpcd.conf","ip_address","static ip_address="+ip+"/24")
		ip=ip.split(".")
		ip=ip[0]+"."+ip[1]+"."+ip[2]+".1"
		self.sustituye("/etc/dhcpcd.conf","routers","static routers="+ip)

		
		host=str(self.lhost.text())
		ip=str(self.lip.text())
		
		
		print(plaza,localidad)
		dat=host+","+ip
		infile = open("/home/pi/Documents/eum/app/expedidora/archivos_config/red.txt", 'w')
		c=infile.write(dat)
		
		self.datosEstacionamiento()
		self.cambia(0)

	def sustituye(self,archivo,buscar,reemplazar):
		"""

		Esta simple función cambia una linea entera de un archivo

		Tiene que recibir el nombre del archivo, la cadena de la linea entera a

		buscar, y la cadena a reemplazar si la linea coincide con buscar

		"""
		with open(archivo, "r") as f:

			# obtenemos las lineas del archivo en una lista

			lines = (line.rstrip() for line in f)
			print(lines)

	 

			# busca en cada linea si existe la cadena a buscar, y si la encuentra

			# la reemplaza

			

			altered_lines = [reemplazar if line==buscar else line for line in lines]
			f= open(archivo, "w+")
			print(altered_lines[0],len(altered_lines))
			for i in range(len(altered_lines)):
				if(buscar in altered_lines[i]):
					print (altered_lines[i])
					cambia=altered_lines[i]
					f.write(reemplazar+"\n")
				else:
					f.write(altered_lines[i]+"\n")
			f.close()
				
				
				
	def configurarPinesGPIO(self):
		botones.configurarPinesGPIO()
		botones.configurarPinesGPIOBobina()

	pantalla = 0
	inicio = 0
	error = 0
	antes = 0
	f1 = f2 = f3 = f4 = f5 = f6 = False
	def leerBotones(self):
		
		global boleto_previo, espera, limite_impresiones,red,green,blue,rrr,cont
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
		#re.setReset()
		self.mostrarFechayHora()
		if self.pantalla == 0:
			#self.stackedWidget.setCurrentIndex(0)
			pass
		elif self.pantalla == 1:
			if espera == 0:
				mixer.init()
				mixer.music.load('/home/pi/Documents/eum/app/expedidora/sonidos/mensaje2.mp3')
				mixer.music.play()
			self.stackedWidget.setCurrentIndex(0)
			espera = espera + 1
			if espera == 25:
				espera = 0
				self.pantalla = 0
		else:
			self.stackedWidget.setCurrentIndex(0)
			espera = espera + 1
			if espera == 25:
				espera = 0
				self.pantalla = 0
		if self.inicio == 0:
			self.error = 0
			self.inicio = 1
			#self.checarFecha()
			self.limpiarBD()
			self.inicioImpresion()
			respuesta = imprimir.footer()
			self.finImpresion()
			if respuesta == "No esta conectada la impresora":
				mensaje = str(noEquipo) + "," + str(4) + "," + str("iniciada")
				validacion = clientes.configSocket("log expedidora")
				clientes.logExpedidora(validacion,"log expedidora",mensaje)
				self.error = 3
				self.pantalla = 1
		if botones.leerAyuda() == 1:
			self.pantalla = 2
		if self.error == 0:
			if boleto_previo == True and self.f1 == False:
				#self.inicioImpresion()
				#respuesta = imprimir.imprimirHeader()
				#self.finImpresion()
				respuesta=1
				if respuesta == "No esta conectada la impresora":
					mensaje = str(noEquipo) + "," + str(4) + "," + str("iniciada")
					validacion = clientes.configSocket("log expedidora")
					clientes.logExpedidora(validacion,"log expedidora",mensaje)
					self.error = 3
					self.pantalla = 1
				else:
					boleto_previo = False
			else:
				if botones.leerMasa() == 1:
					if self.f1 == False:
						print("------Presencia Auto --------")
						self.f1 = botones.leerBotonesEntrada()
					if self.f1 == True and self.f2 == False and self.f3 == False and self.f4 == False and self.f5 == False:
						if boleto_previo == False:
							noBolF = folio.saberFolio()
							folioBD = noBolF
							fechaIn	= fechaUTC.fechaConFormato()
							horaEnt = fechaUTC.tiempoConFormato()
							fechatimestamp = str(fechaIn)+" "+str(horaEnt)
							#self.insertarBoleto(plaza,noEquipo,noBolF,fechatimestamp,'DEFAULT-ESCOM')
							''' Operacion 1.- Registro de boleto'''
							#mensaje = (idBoleto,idExpedidora,FechaExpedicion, idestado, idtipodescuento, idSalida)
							mensaje = noBolF + "," + str(noEquipo) + "," + fechatimestamp + "," + str(1) + "," + str(1) + "," + str(0)
							validacion=1
							print("validacion",validacion)
							#if validacion == "error":
							#	self.f1 = self.f2 = self.f3 = self.f4 = self.f5 = False
							#	self.pantalla = 1
							conexionServ=os.system("ping -c 1 192.168.1.129")
							print("conexionServ",conexionServ)
							#if validacion == "error":
							if conexionServ != 0:
								valor = 1
								
								if valor == "error":
									self.f1 = self.f2 = self.f3 = self.f4 = self.f5 = False
									self.pantalla = 1
								else:
									self.insertarBoleto(plaza,noEquipo,noBolF,fechatimestamp,'DEFAULT-ESCOM')
									folio.escribirArchivoFolios(noBolF)
									self.inicioImpresion()
									#respuesta = imprimir.imprimirHeader()
									respuesta = imprimir.imprimirQR2(noBolF,str(3),str(fechaIn),str(horaEnt))
									self.finImpresion()
									if respuesta == "No esta conectada la impresora":
										mensaje = str(noEquipo) + "," + str(4) + "," + str("iniciada")
										#validacion = clientes.configSocket("log expedidora")
										#clientes.logExpedidora(validacion,"log expedidora",mensaje)
										self.error = 3
										self.pantalla = 1
									else:

										if(respuesta=="ack"):
											papel_cont = self.conteoBoletos()
											if papel_cont == limite_impresiones:
												#MANDAR MENSAJE AL SERVIDOR DE PAPEL CASI AGOTADO
												mensaje = str(noEquipo) + "," + str(3) + "," + str("iniciada")
												#validacion = clientes.configSocket("log expedidora")
												#clientes.logExpedidora(validacion,"log expedidora",mensaje)
											papel_cont = papel_cont + 1
											self.aumentoConteo(papel_cont)
											
											mixer.init()
											mixer.music.load('/home/pi/Documents/eum/app/expedidora/sonidos/mensaje1.mp3')
											mixer.music.play()
											boleto_previo = True
											self.f2 = True
										else:
											print("PRESIONE NUEVAMENTE")
							else:
								validacion = clientes.configSocket("registro boleto")
								valor = clientes.enviarMensaje(validacion,mensaje)
								if valor == "error":
									self.f1 = self.f2 = self.f3 = self.f4 = self.f5 = False
									self.pantalla = 1
								else:
									self.insertarBoleto(plaza,noEquipo,noBolF,fechatimestamp,'DEFAULT-ESCOM')
									folio.escribirArchivoFolios(noBolF)
									self.inicioImpresion()
									#respuesta = imprimir.imprimirHeader()
									respuesta = imprimir.imprimirQR2(noBolF,str(noEquipo),str(fechaIn),str(horaEnt))
									self.finImpresion()
									if respuesta == "No esta conectada la impresora":
										mensaje = str(noEquipo) + "," + str(4) + "," + str("iniciada")
										validacion = clientes.configSocket("log expedidora")
										clientes.logExpedidora(validacion,"log expedidora",mensaje)
										self.error = 3
										self.pantalla = 1
									else:
										if(respuesta=="ack"):
											papel_cont = self.conteoBoletos()
											if papel_cont == limite_impresiones:
												#MANDAR MENSAJE AL SERVIDOR DE PAPEL CASI AGOTADO
												mensaje = str(noEquipo) + "," + str(3) + "," + str("iniciada")
												validacion = clientes.configSocket("log expedidora")
												clientes.logExpedidora(validacion,"log expedidora",mensaje)
											papel_cont = papel_cont + 1
											self.aumentoConteo(papel_cont)
											mixer.init()
											mixer.music.load('/home/pi/Documents/eum/app/expedidora/sonidos/mensaje1.mp3')
											mixer.music.play()
											boleto_previo = True
											self.f2 = True
										else:
											print("PRESIONE NUEVAMENTE")
				if self.f2 == True and self.f3 == False and self.f4 == False  and self.f5 == False:
					if self.f6 == False:
						time.sleep(0.5)
						botones.abrir()
						print("ABRIENDO....................")
						cont=cont+1
						print("////////Boletos: ",cont)
						self.f6 = True
					self.f3 = botones.leerBobina2Subida()
					#self.f3 = True;
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
			#respuesta = imprimir.imprimirHeader()
			if respuesta == "ack":
				boleto_previo = False
				self.error = 0
		elif self.error == 3:
			respuesta = imprimir.instanciarImpresora()
			if respuesta != "No esta conectada la impresora":
				self.error = 0
		QtCore.QTimer.singleShot(100, self.leerBotones)

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
		hora = fechaUTC.tiempoConFormato()
		self.ldate.setText(fecha)
		self.ltime.setText(hora)

	def apagarRasp(self):
		os.system("sudo shutdown -P 0")

	def reiniciarRasp(self):
		os.system("sudo shutdown -r 0")



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
				mensaje = str(noEquipo) + "," + str(1) + "," + str("iniciada")
				validacion = clientes.configSocket("log expedidora")
				clientes.logExpedidora(validacion,"log expedidora",mensaje)
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
					mensaje = str(noEquipo) + "," + str(2) + "," + str("iniciada")
					validacion = clientes.configSocket("log expedidora")
					clientes.logExpedidora(validacion,"log expedidora",mensaje)
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
			return plaza,localidad
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

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
			return plaza,localidad
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)

		
		
		
def obtenerTerminal():
	global noEquipo
	try:
		connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
		with connection.cursor() as cursor:
			cursor.execute(
				' SELECT num_expedidora FROM datos_expedidora WHERE id_expedidora = 1')
			row = cursor.fetchone()
			if row is not None:
				noEquipo = int(row[0])
				connection.commit()
				connection.close()
			return noEquipo
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
	global localidad,plaza,noEquipo
	infile = open('/home/pi/Documents/eum/app/expedidora/archivos_config/datos.txt','r')
	datos= infile.readline()
	arr=datos.split(',')
	plaza=arr[0]
	localidad=arr[1]
	noEquipo=arr[2]
	infile.close()
	
	image = Image.open('/home/pi/Documents/eum/app/expedidora/logo.png')
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', size=16)
	 
	(x, y) = (60, 40)
	message1 = plaza
	color = 'rgb(0, 0, 0)' # black color		 
	draw.text((x, y), message1, fill=color, font=font)
	(x, y) = (60, 60)
	message2 = localidad
	draw.text((x, y), message2, fill=color, font=font)
	(x, y) = (60, 10)
	message3 = "¡BIENVENIDO!"
	font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', size=22)
	draw.text((x, y), message3, fill=color, font=font)
	image.save('/home/pi/Documents/eum/app/expedidora/logoPT.png')
	obtenerTerminal()
	obtenerPlazaYLocalidad()
	hilos()
