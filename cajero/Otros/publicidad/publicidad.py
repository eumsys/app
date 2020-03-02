import sys
import os
import time
import fechaUTC as hora
from threading import Timer,Thread
import sched
import termios
import serial
import binascii
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox
from PyQt5 import QtCore, QtGui, uic
from datetime import datetime, timedelta
import calendar
import psycopg2, psycopg2.extras
import leerBotones as botones
#from pygame import mixer
import pygame 
import sys


conn = psycopg2.connect(database='CajerOk',user='postgres',password='Postgres3UMd6', host='localhost')
cur = conn.cursor()
kill = 0
configurandoPublicidad=0
def interface():
	class Ventana(QDialog):
		conteo_final=0
		global gui,total,conn,cur,nivelActual,NoCajero
		def __init__(self):
			QDialog.__init__(self)
			gui=uic.loadUi("/home/pi/Documents/eum/app/cajeroF/publicidad/uiPub.ui", self)
			gui.leerBotones()
			self.cambia(0)
			self.bquitar.clicked.connect(self.elimina2)
			self.bsalir.clicked.connect(self.saliendoConfiguracion)
			self.bhabilitar.clicked.connect(self.habilitaTarifa)
			self.bapagar.clicked.connect(self.apagando)
			self.bapagar.setShortcut("ESCAPE")
			self.idpub2.valueChanged.connect(self.actualizaMensaje)
			self.idpub1.valueChanged.connect(self.actualizaMensaje2)
			self.tablapublicidad.setColumnCount(4)
			self.tablapublicidad.setHorizontalHeaderLabels(['','Id','Posicion','Ruta'])
			botones.configurarPinesGPIO()
			#self.llenaTabla()
				
		def apagando(self):
			os.system("sudo shutdown 0")
		def saliendoConfiguracion(self):
			global configurandoPublicidad
			botones.limpiar()
			configurandoPublicidad=0
			self.cambia(0)
			
		def leerBotones(self):
			global configurandoPublicidad
			#botones.configurarPinesGPIO()
			menuPublicidad = botones.leerBotonesEntrada()
			#botones.limpiar()
			"""print("VAL:",menuPublicidad)
			if(menuPublicidad==True):
				configurandoPublicidad=1
				self.cambia(1)"""
			
			QtCore.QTimer.singleShot(100, self.leerBotones)
		
		def cambia(self,num):
				self.stackedWidget.setCurrentIndex(num)
				
		def llenaTabla(self):
				global cur
				cur.execute("select * from \"PUBLICIDAD\" order by posicion Asc")
				rowc=self.tablapublicidad.rowCount()
				k=0
				while(k<rowc):
					self.tablapublicidad.removeRow(0)
					#del self.CB2[0]
					k=k+1
				row=0
				for reg in cur: 
					#print(reg[0],reg[1],reg[2],reg[3],reg[4],reg[5],reg[6],reg[7],reg[8],reg[9],reg[10],reg[11])
					self.tablapublicidad.insertRow(row)
					idp=QTableWidgetItem(str(reg[0]))
					pos=QTableWidgetItem(str(reg[1]))
					ruta=QTableWidgetItem(str(reg[2]))
					
					if(reg[3]==1):
						state=QTableWidgetItem("Habilitada")
					else:
						state=QTableWidgetItem("Deshabilitada")
					self.tablapublicidad.setItem(row,0,state)
					self.tablapublicidad.item(row,0).setTextAlignment(4)
					
					self.tablapublicidad.setItem(row,1,idp)
					self.tablapublicidad.item(row,1).setTextAlignment(4)
					self.tablapublicidad.setItem(row,2,pos)
					self.tablapublicidad.item(row,2).setTextAlignment(4)
					self.tablapublicidad.setItem(row,3,ruta)
					self.tablapublicidad.item(row,3).setTextAlignment(4)
					row=row+1
					
		def habilitaTarifa(self):
				global cur,conn
				idp=self.idpub2.value()
				fecha=hora.mostrarFechayHora()
				vac=0
				cur.execute("select estado from \"PUBLICIDAD\" where \"idPublicidad\"="+str(idp))
				for reg in cur: 
					vac=reg[0]
					print(reg[0])
				
				if(vac==0):
					
					cur.execute("update \"PUBLICIDAD\" set estado=1 where \"idPublicidad\"="+str(idp))
					self.bhabilitar.setText("Deshabilitar")
					conn.commit()
				else:
					cur.execute("update \"PUBLICIDAD\" set estado=0 where \"idPublicidad\"="+str(idp))
					self.bhabilitar.setText("Habilitar")
					conn.commit()
					
				
				self.llenaTabla()
		
		def elimina2(self):
				global cur,conn
				fecha=hora.mostrarFechayHora()
				idp=self.idpub.value()
				print("Eliminado Caon")
				cur.execute("delete from \"PUBLICIDAD\" where \"idPublicidad\"="+str(idp))
				conn.commit()
				self.llenaTabla()
				
		def actualizaMensaje(self):
				global cur
				vac=2
				idt=self.idpub2.value()
				cur.execute("select estado from \"PUBLICIDAD\" where \"idPublicidad\"="+str(idt))
				for reg in cur: 
					vac=reg[0]
					print(reg[0])
				if(vac==1):
					self.bhabilitar.setEnabled(True)
					self.bhabilitar.setText("Deshabilitar")
					print("simon1")
				if(vac==0):
					self.bhabilitar.setEnabled(True)
					self.bhabilitar.setText("Habilitar")
					
					print("simon0")
				if(vac==2):
					self.bhabilitar.setEnabled(False)
					self.bhabilitar.setText("No existente")
					print("simon2")
					
		def actualizaMensaje2(self):
				global cur
				vac=2
				idt=self.idpub1.value()
				cur.execute("select estado from \"PUBLICIDAD\" where \"idPublicidad\"="+str(idt))
				for reg in cur: 
					vac=reg[0]
					print(reg[0])
				if(vac==2):
					self.bquitar.setEnabled(False)
					self.bquitar.setText("No existente")
					print("K1",vac)
				else:
					self.bquitar.setEnabled(True)
					self.bquitar.setText("Eliminar")
					print("K2",vac)
					
	app = QApplication(sys.argv)
	_ventana = Ventana()
	_ventana.show()
	app.exec_()
	
def reproduceVideo():
		global cur
		#idt=self.idpub1.value()
		while(1):
			if(configurandoPublicidad==0):
				os.system("lsblk > aok.txt")
				f = open("aok.txt")
				linea = f.readline()
				l=''

				while linea != "":
					linea = f.readline()
					if('disk' in linea):
						print('m1')
						particion=linea.split(' ')
						part=particion[0]
						if('sd' in part):
							os.system('sudo mount /dev/'+part+'1 /media/pi/KINGSTON')
					if('/media'in linea):
						print('m2')
						l=linea
						break
				f.close()
				if(l):
					print('USBB Conectada')
					parts=l.split('part ')
					USB=parts[1]
					print('USBB Conectada',parts[1])
					if USB[-1] == '\n':
						USB = USB[:-1]
					a="ls "+str(USB)+" > aok2.txt"
					print(a)
					os.system(a)
					f = open("aok2.txt")
					linea = f.read()
					f.close()
					videos= linea.split('\n')
					print('Cantidad de videos:',len(videos)-1,videos)
					for video in videos:
						if(video):
							print('m',video)
							ruta=str(USB)+str("/"+video)
							#j=os.system("omxplayer -o local --win \"0 0 800 1360\" "+ruta+"")
							#j=os.system("lxterminal --geometry=100x2 -e omxplayer -o local --win \"0 0 800 1360\" "+ruta+"")
							j=os.system("lxterminal --geometry=100x2 -e omxplayer -o local --win \"0 0 1100 1700\" "+ruta+"")
				
							if(j==768):
								print(j)
								return
							if(j==256):
								print("VIDEO NO ENCONTRADO")
							else:
								print("VIDEO REPRODUCIDO: ",video)
				else:
					time.sleep(1)
					print('Conecte su usb')
				
			
				
	
	
if __name__ == "__main__":
	thread1 = Thread(target=interface,args=())
	thread2 = Thread(target=reproduceVideo, args = ())

	try:
		pass
		thread1.start()
		thread2.start()

		
		
		
	except Exception as e:
		pass

	while(thread1.is_alive()):
		kill = 0
	kill = 1
	
	print("termine")

