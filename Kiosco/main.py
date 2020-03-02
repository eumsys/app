import sys
import os
import time
import sched
import psycopg2
from threading import Timer,Thread
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox
from PyQt5 import QtCore, QtGui, uic
import calendar
import cliente as cliente

clock = sched.scheduler(time.time, time.sleep)

global ser
kill = 0
killer = 0
leido = 0
banderaServer=0
secs=0
fo=""
fe=""
pe=""
hh=""
hsalida=""
var=0
plaza=""
localidad=""

def interface():
	class Ventana(QDialog):
		def __init__(self):
			QDialog.__init__(self)
			gui = uic.loadUi("/home/pi/Documents/eum/app/Kiosco/Interfaces/kiosco.ui", self) #Se utiliza la ruta completa para el boot
			self.cambia(0)
			self.loopFunction()
			self.contadorSegundos()
			self.desactivarBotones()
			
			self.nomPlaza_6.setText(plaza)
			self.nomLoc_6.setText(localidad)
			self.nomPlaza_3.setText(plaza)
			self.nomLoc_3.setText(localidad)
			self.label_3.setVisible(False)
			
			self.bnConfirmarDesc.clicked.connect(self.aplicarDescuento)
			self.bnCancelarDesc.clicked.connect(self.cancelarDescuento)
			self.bnCerrarSesion.clicked.connect(lambda:self.cambia(0))
			self.lineContrasena.setEchoMode(QLineEdit.EchoMode(2))
			self.bnApagar.clicked.connect(self.apagarRasp)
			self.bnApagar_2.clicked.connect(self.apagarRasp)

			
			self.bn1.clicked.connect(lambda:self.tecladoSum(1))
			self.bn2.clicked.connect(lambda:self.tecladoSum(2))
			self.bn3.clicked.connect(lambda:self.tecladoSum(3))
			self.bn4.clicked.connect(lambda:self.tecladoSum(4))
			self.bn5.clicked.connect(lambda:self.tecladoSum(5))
			self.bn6.clicked.connect(lambda:self.tecladoSum(6))
			self.bn7.clicked.connect(lambda:self.tecladoSum(7))
			self.bn8.clicked.connect(lambda:self.tecladoSum(8))
			self.bn9.clicked.connect(lambda:self.tecladoSum(9))
			self.bn0.clicked.connect(lambda:self.tecladoSum(0))
			self.bnBorrarTexto.clicked.connect(lambda:self.tecladoSum(10))
			self.bnLimpiarTexto.clicked.connect(lambda:self.tecladoSum(11))
			self.bnIniciarSesion.clicked.connect(lambda:self.tecladoSum(12))
			
			self.lineIdEmpleado.editingFinished.connect(self.seleccion_cambiada)
			self.lineContrasena.editingFinished.connect(self.seleccion_cambiada2)
		
		def activarBotones(self):
			self.bnConfirmarDesc.setEnabled(True)
			self.bnConfirmarDesc.setText("CONFIRMAR DESCUENTO")
			self.bnCancelarDesc.setEnabled(True)
			self.bnCancelarDesc.setText("CANCELAR DESCUENTO")
			
		def desactivarBotones(self):
			self.bnConfirmarDesc.setEnabled(False)
			self.bnConfirmarDesc.setText("INSERTAR BOLETO")
			self.bnCancelarDesc.setEnabled(False)
			self.bnCancelarDesc.setText("INSERTAR BOLETO")
			
		def seleccion_cambiada(self):
			global var
			var=1

		def seleccion_cambiada2(self):
			global var
			var=2
			
		def apagarRasp(self):
			print("apagando...")
			os.system("sudo shutdown -P 0")
			
		def tecladoSum(self,val):
			global var
			if(val==10 and var==1):														#Borrar el ultimo caracter
				idUser=self.lineIdEmpleado.text()[0:-1]
				self.lineIdEmpleado.setText(idUser)
			elif(val==10 and var==2):
				pasw=self.lineContrasena.text()[0:-1] 
				self.lineContrasena.setText(pasw)
			elif(val==11 and var==1):													#Limpiar el campo de texto
				self.lineIdEmpleado.setText("")
			elif(val==11 and var==2):
				self.lineContrasena.setText("")
			elif(val>=0 and val<=9 and var==1):										#Simbolos numericos para iniciar sesión
				self.lineIdEmpleado.setText(self.lineIdEmpleado.text()+str(val))
			elif(val>=0 and val<=9 and var==2):
				self.lineContrasena.setText(self.lineContrasena.text()+str(val))
			elif(val==12):																#Inicio de sesion
				#FUNCION PARA INICIAR SESION
				mensajePsw=self.lineContrasena.text()
				mensajeIdUser=self.lineIdEmpleado.text()
				#print(mensajePsw)
				#print(mensajeIdUser)
				mensaje = str(mensajeIdUser) + "," + str(mensajePsw)
				self.lineContrasena.setText("")
				self.lineIdEmpleado.setText("")
				algo=cliente.configSocket("inicio sesion",mensaje)
				print("Eetoy en MAIN:",algo)
				if(algo=="Inicio de \nSesion Exitoso"):
					self.cambia(1)
					self.label_3.setVisible(False)
				else:
					self.label_3.setVisible(True)
				
		def cambia(self,num):
			self.stackedWidget.setCurrentIndex(num)

		def loopFunction(self):
			global leido
			self.label_9.setText(time.strftime("%H:%M:%S"))
			self.label_10.setText(time.strftime("%d-%m-%Y"))
			self.label_30.setText(time.strftime("%H:%M:%S"))
			self.label_29.setText(time.strftime("%d-%m-%Y"))
			if(leido == 1):
				leido = 0
				self.activarBotones()
			QtCore.QTimer.singleShot(5,self.loopFunction)

		def contadorSegundos(self):
			global banderaServer, secs
			if(banderaServer==1):
				secs=secs+1
				if(secs==4):
					self.mensajeServer.setText("")
					secs=0
					banderaServer=0
			QtCore.QTimer.singleShot(1000,self.contadorSegundos)
					
		def aplicarDescuento(self):
			global leido,killer,banderaServer,folio,inTerminal,inFecha,inHora
			self.desactivarBotones()
			tipoDescuento=2									#(Cinemex)
			mensaje=str(folio)+","+str(inTerminal)+","+str(inFecha)+" "+str(inHora)+","+str(tipoDescuento)
			algo=cliente.configSocket("descuento a aplicar",mensaje)
			#print("Mensaje del servidor: ",algo)
			self.mensajeServer.setText(algo)
			banderaServer=1
			leido=0
			killer=0
			
		def cancelarDescuento(self):
			global leido,killer
			self.desactivarBotones()
			killer=0
			leido=0			
			
	app = QApplication(sys.argv)
	_ventana = Ventana()
	_ventana.show()
	app.exec_() 
	
def leerArchivo():
	global leido,kill,killer,folio,inTerminal,inFecha,inHora
	while(kill == 0):
		while(killer == 0 and kill == 0):
			leerArch = open("/home/pi/Documents/eum/app/Kiosco/archivosTXT/ticket.txt", "r")
			folio=''
			folio=leerArch.readline().rstrip("\n")
			time.sleep(.2)
			leido=0
			if(folio != ''):													#Si existe algun folio
				if(str("Estacionamientos unicos de Mexico") in str(folio)):	#Si el folio pertenece al estacionamiento
					
					leido=1
					killer = 1
					leerArch.close()
					leerArch = open("/home/pi/Documents/eum/app/Kiosco/archivosTXT/ticket.txt", "r")

					leyenda=(leerArch.readline().rstrip("\n")).lstrip("\x00")	#Estacionamientos unicos de mexico
					folio=(leerArch.readline().rstrip("\n")).lstrip("\x00")		#id del boleto
					inTerminal=leerArch.readline().rstrip("\n")					#id expedidora
					inFecha=leerArch.readline().rstrip("\n")					#fecha entrada dd/mm/aaaa
					inHora=leerArch.readline().rstrip("\n")						#hora entrada hh:mm:ss
					
					leerArch.close()
					leerArch = open("/home/pi/Documents/eum/app/Kiosco/archivosTXT/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()
				else:															#Si el folio no pertenece al estacionamiendo borro el archivo
					leerArch.close()
					leerArch = open("/home/pi/Documents/eum/app/Kiosco/archivosTXT/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()
			else:				#Si no existe ningun folio 
				leerArch.close()

def leerCodQR():
	lee = os.system("zbarcam --raw --prescale=10x10  /dev/video0 > /home/pi/Documents/eum/app/Kiosco/archivosTXT/ticket.txt")
	
def obtenerPlazaYLocalidad():
	global plaza, localidad
	usuario = 'postgres'
	contrasenia = 'Postgres3UMd6'
	bd = "dbeum_tecamac"
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

if __name__ == "__main__":
	
	#INICIALIZAMOS EL HILO DE LA INTERFAZ
	obtenerPlazaYLocalidad()
	thread1 = Thread(target=interface,args=())
	thread3 = Thread(target=leerCodQR, args = ())
	thread4 = Thread(target=leerArchivo, args=())
	try:
		thread1.start()
		thread3.start()
		time.sleep(.4)
		thread4.start()
		
	except Exception as e:
		pass

	while(thread1.is_alive()):
		kill = 0
	kill = 1
	
	thread3.kill()
	print("\nTermine")
