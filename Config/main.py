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

ruta =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
ruta = ruta + "/"


def obtenerUsuario(ruta):
	lista = ruta.split("/")
	return "/"+lista[1]+"/"+lista[2]+"/"
	
	
rutaUsuario = obtenerUsuario(ruta)
print(rutaUsuario)



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

tipos = ["expedidora","cajero","salida","publicidad"]



def interface():
	class Ventana(QDialog):
		def __init__(self):
			self.SO_COMPATIBLES = ['Ubuntu','Raspbian']
			QDialog.__init__(self)
			gui = uic.loadUi(ruta+"Interfaces/config.ui", self) #Se utiliza la ruta completa para el boot
			self.cambia(0)
			self.loopFunction()
			self.obtenerConfiguracion()
			#self.cambiarConfiguracion()
			self.bconfirmar.clicked.connect(self.cambiarConfiguracion)
			self.bsalir.clicked.connect(self.salir)
			self.bsalir2.clicked.connect(self.salir)
			self.bvolver.clicked.connect(lambda:self.cambia(0))
			


		def obtenerSO(self):
			#Osys = os.system("hostnamectl | grep 'Operating System'")
			Osys = os.popen("hostnamectl | grep 'Operating System'").read()
			for so in self.SO_COMPATIBLES:
				if so in Osys:
					print("Systema compatible:", so)
					break
				else:
					so = 0
			if so:
				return so
			else:
				print("Systema no compatible")
				exit(0)



		def sustituye(self,archivo,buscar,reemplazar):
			"""
			Sustituye una linea de un archivo por otra
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
						#print (altered_lines[i])
						cambia=altered_lines[i]
						f.write(reemplazar+"\n")
					else:
						f.write(altered_lines[i]+"\n")
				f.close()
			
			
		
			
		def salir(self):
			exit(0)

		def obtenerConfiguracion(self):
			global equipo, sucursal, tipo
			try:
				infile = open(rutaUsuario+"eum.conf", 'r')
				c=infile.readline()
				arr=c.split(',')
				equipo=int(arr[0])
				sucursal=int(arr[1])
				tipo=int(arr[2])
				infile.close()
			except:
				equipo=1
				sucursal=1
				tipo=0
				infile = open(rutaUsuario+"eum.conf", "w")
				infile. write(str(equipo)+","+str(sucursal)+","+str(tipo))
				infile. close()
			print("equipo,sucursal,tipo ",equipo,sucursal,tipo)
			self.equipo.setValue(equipo)
			self.sucursal.setValue(sucursal)
			self.tipo.setCurrentIndex(tipo)

		def cambiarConfiguracion(self):
			global equipo, sucursal, tipo
			equipo = self.equipo.value()
			sucursal = self.sucursal.value()
			tipo = self.tipo.currentIndex()
			aplicacion = ""

			data = str(equipo)+","+ str(sucursal)+","+ str(tipo+1)
			infile = open(rutaUsuario+"eum.conf", 'w')
			c=infile.write(data)
			infile.close()
			so = self.obtenerSO()
			if so == self.SO_COMPATIBLES[0]:
				os.system("echo eum | sudo -S chmod 777 /etc/netplan/01-network-manager-all.yaml")
				self.sustituye("/etc/netplan/01-network-manager-all.yaml","addresses: [192","      addresses: [192.168.1."+str(tipo+1)+str(equipo)+"/24]")
				if tipo == 1:
					aplicacion = ruta+"../"+"expedidora/first.py"
				elif tipo == 2:
					aplicacion = ruta+"../"+"Inicio.py"
				elif tipo == 3:
					aplicacion = ruta+"../"+"salida/salida.py"
				elif tipo == 4:
					aplicacion = ruta+"../"+"publicidad/publicidad.py"
				self.sustituye(".bashrc","python3","python3 "+aplicacion)
			elif so == self.SO_COMPATIBLES[1]:
				self.sustituye("/etc/dhcpcd.conf","static ip_address="," static ip_address=192.168.1."+str(tipo+1)+str(equipo)+"/24]")
				if tipo == 1:
					aplicacion = ruta+"../"+"expedidora/first.py"
				elif tipo == 2:
					aplicacion = ruta+"../"+"cajeroF/cajero/cajeroRed.py"
				elif tipo == 3:
					aplicacion = ruta+"../"+"salida/salida.py"
				elif tipo == 4:
					aplicacion = ruta+"../"+"publicidad/publicidad.py"
				self.sustituye(rutaUsuario+".bashrc","python3","sudo python3 "+aplicacion)
			self.obtenerConfiguracion()
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Es necesario reiniciar el equipo para aplicar los cambios")
			msg.setInformativeText("¿ Desea reiniciar ?")
			msg.setWindowTitle("Configuracion completa")
			msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
			msg.buttonClicked.connect(msgbtn)
			retval = msg.exec_()
			#self.cambia(1)


		
		def seleccion_cambiada(self):
			global var
			var=1

		def seleccion_cambiada2(self):
			global var
			var=2
			
		
				
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
					
		
	app = QApplication(sys.argv)
	_ventana = Ventana()
	_ventana.show()
	app.exec_() 


def msgbtn(i):
	response = i.text()
	print(response)
	if("Yes" in response): 
		print("Reiniciando...")
		os.system("reboot")
	else:
		print("Cancelado...")
		exit(0)
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
	#obtenerPlazaYLocalidad()
	thread1 = Thread(target=interface,args=())
	try:
		thread1.start()
		#thread3.start()
		time.sleep(.4)
		
	except Exception as e:
		pass

