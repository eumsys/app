# coding=utf-8
#!/usr/bin/env python3

'''
Version: MB-2.1
Fecha: 26/12/2019

UPDATE:
- Scanner validacion directa.

INSTALACION :
- crear archivos: /home/cajero/Documentos/ticket.txt'
'''
import sys
import os
import time
import fechaUTC as hora
#import Conexiones.cliente as Servidor
#from pygame import mixer
import subprocess
#import imprimirBoleto as impresora
from threading import Timer,Thread 
import sched
import termios
import serial
import binascii
from bitstring import BitArray
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox
from PyQt5 import QtCore, QtGui, uic
from datetime import datetime, timedelta
import calendar
import psycopg2, psycopg2.extras
from Botones.Botones import Botones,PuertoDeComunicacion, obtenerNombreDelPuerto
from Pila.Pila import Pila
from Comunicacion import Comunicacion
from struct import *

#ruta = os.path.join(os.path.dirname(__file__))
#sys.path.append(ruta)
#ruta = ruta + "/"

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador
from Monitor.Hopper import Hopper
from PuertoSerie import PuertoSerie
import traceback
from Logs.GuardarLogs import GuardarLogs
import shutil




ruta =  os.path.join(os.path.dirname(os.path.abspath(__file__)))
ruta = ruta + "/"
def obtenerUsuario(ruta):
	lista = ruta.split("/")
	return "/"+lista[1]+"/"+lista[2]+"/"	
rutaUsuario = obtenerUsuario(ruta)
print(rutaUsuario)
print(rutaUsuario[6:-1])
usuario = rutaUsuario[6:-1]

raiz =  os.path.join(os.path.dirname(os.path.abspath(__file__)),"../..")
sys.path.append(raiz)

import Conexiones.cliente as Servidor
from Conexiones.Conexiones import Conexiones

'''DL17'''
from encriptacionQR import codificar
#from Monitor.Controladora import Controladora,ListaDeVariables
from configParser.viewData import viewData
'''DL17'''



PATH_ARCHIVO_CONFIGURACION_TERMINAL_SERIAL=rutaUsuario+"numeroSerial.txt"

clock = sched.scheduler(time.time, time.sleep)
cp=0
#global ser
DA=1166
Sinpago=0
ser=0
total = 0
bill = 0
a=0
ma=0
factorDeEscala = .10
tarifa=1
aux_tarifa=0
cambio=0
aux_cambio = 0
aux_cambio1 = 0
estatus=0
rep=0
kill = 0
killer = 0
kill_aux = 0
killbill=0
leido = 0
cajeroSuspendido=0
conteoPantallaPrincipal = 0
aux_tarifa1 =0
aux_dif=""
fo=""
fe=""
pe=""
costillo=0
hh=""
hsalida=""
avis=""
pagado=0
w=0
mona=0
mond=0
cs1=0
cs2=0
config=0
ser=0
monedas=[85,78,69,58]
monedasPago=[0,0,0,0]
monedasCambio=[0,0,0,0]
billetesPago=[0,0,0,0]
tarifasAplicadas=""
monedasTotal=290
dineroTotal=1166
dineroTotalB=0
billetesTotales=0
billetes=[0,0,0,0]
mensajeBoletoUsado=0
mensajeBoletoSellado=0
mensajeBoletoPerdido=0
mensajeError=0
suspenderCajero=0
cambio_faltante=0
tiempoBillExc=0
tiempoLimBill=0
tl=0
mensajeAyuda=0
cartuchoRemovido=0
preguntarPorEstado=0
mostrarTiempoDeSalidaRestante=[0,'']
conn = psycopg2.connect(database='CajerOk',user='postgres',password='Postgres3UMd6', host='localhost')
cur = conn.cursor()
tarifaVoluntaria=0
vvol=""
comienzaCambio=0
nivelDeCambio=0
nivelActual=[0,0,0,0]
nom=""
loc=""
contadorCartuchos=1
opcionAdmin=0
cambiaColor=0
imprime=0
accesoAcaja=0
inicioPago=0
tiempoAgotadoDePago=0
y=0
z=0
p=0
w=0
q=0
v=0
c=0
sel=0
USUARIO=0
correoUSUARIO=""
NoCajero=0
tarifaSeleccionada=0
varc=0
#red=117
#green=248
#blue=148
rrr=0
"""red=59
green=109
blue=153
"""
red=125
green=181
blue=215
comienzaLectura=0
varl=0
comienzaCobro=0
registraPago=0


configuracion = []
camInicial=''
USUARIO=''
host=''
ip=''
plaza = ""
localidad = ""
user="eum"
pswd="pi"

valoresMonedas=[1,2,5,10]
valoresBilletes=[20,50,100,200]
MONEDAS_POR_HW = [0,0,0,0]
MONEDAS_POR_SW = [85,78,69,58]
conexion_activa = False
aportacionConfirmada=0

OP_EXITOSA = 1
OP_CAMBIO_INCOMPLETO = 2
OP_CAMBIO_INCOMPLETO_SUSPENDIDO = 3
OP_EXITOSA_SUSPENDIDO = 4
OP_CANCELADA = 5
OP_CANCELADA_CAMBIO_INCOMPLETO = 6
OP_CANCELADA_CAMBIO_INCOMPLETO_SUSPENDIDO = 7
OP__CANCELADA_SUSPENDIDO = 8


CobroFinalizado = 0

equipo = 0
sucursal = 0 
tipo = 0
Boleto = ""


tipo_controladora = 0
encriptacion = 0

guardar = GuardarLogs("Logs")

sensores = viewData('sensores.ini')
secuencia_recarga = 0

FALTANTE = ["-","-","-","-","-"]

def interface():
	class Ventana(QDialog):
		conteo_final=0
		global ser,gui,total,conn,cur,nivelActual,NoCajero,cp,sensores
		def __init__(self):
			QDialog.__init__(self)
			gui = uic.loadUi(ruta+"rb.ui", self)
			#Leyendo stream de video...
			self.obtenerConfiguracion()
			self.secuenciaCobro(0)
			self.montos()
			self.pollingConexion()
			self.logPrender()
			#gui.leerBotones()
			#gui.boleto_leido()
			gui.contadorSegundos()
			gui.contadorMiliSegundos()
			fehoy=str(datetime.now().date()).split('-',2)
			fehoy=fehoy[2]+"/"+fehoy[1]+"/"+fehoy[0]
			#self.ldate.setText(fehoy)
			self.ldate2.setText(fehoy)

			self.current_timer = None
			self.prioridad=0
			#self.alerta.setVisible(False)
			self.lerror1.setVisible(False)

			self.salirAdmin.clicked.connect(self.saliendoAdmin)

			self.bntarifa.clicked.connect(lambda:self.cambia(7))
			self.bcancelar.clicked.connect(lambda:self.cambia(6))
			self.benter.setShortcut('Return')
			self.bcancelarPago.setShortcut('c')
			self.bsalirTarifas.clicked.connect(lambda:self.cambia(9))
			self.bsalirntarifas.clicked.connect(lambda:self.cambia(9))
			self.bconfirmartarifa.clicked.connect(self.tarifaConfirmada)
			self.bquitar.clicked.connect(self.elimina2)
			self.bhabilitar.clicked.connect(self.habilitaTarifa)
			self.bconfirmavol.clicked.connect(self.volConfirmado)
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
			self.bnborrar.clicked.connect(lambda:self.tecladoSum(10))
			#self.lnom.editingFinished.connect(lambda:self.holi(3))
			#self.llol.editingFinished.connect(lambda:self.holi(6))

			#self.bconfirmarplaza.clicked.connect(self.cambiaNombre)
			self.salirplaza.clicked.connect(lambda:self.cambia(9))
			self.salirCalibracion.clicked.connect(self.finalizarCalibracion)
			self.salirCajon.clicked.connect(self.finalizarCorteCaja)
			self.salirAyuda.clicked.connect(self.finalizarSoporteTecnico)
			self.salirReportes.clicked.connect(lambda:self.cambia(9))
			self.bsalirLogin.clicked.connect(lambda:self.cambia(9))
			self.idtar2.valueChanged.connect(self.actualizaMensaje)
			self.idtar1.valueChanged.connect(self.actualizaMensaje2)

			"""self.btarifas.clicked.connect(self.seccionTarifas)
			self.bcorte.clicked.connect(self.cortandoLaCaja)
			self.bcalibracion.clicked.connect(self.calibrando)
			self.bplaza.clicked.connect(self.llenaCamposPlaza)
			self.bpapel.clicked.connect(self.reemplazoPapel)
			self.bpublicidad.clicked.connect(self.menuPublicidad)
			self.breporte.clicked.connect(lambda:self.cambia(12))
			"""
			self.btarifas.clicked.connect(lambda:self.mueveyManda(1))
			self.bcorte.clicked.connect(lambda:self.mueveyManda(2))
			self.bcalibracion.clicked.connect(lambda:self.mueveyManda(3))
			self.bplaza.clicked.connect(lambda:self.mueveyManda(4))
			self.bpapel.clicked.connect(lambda:self.mueveyManda(5))
			self.bpublicidad.clicked.connect(lambda:self.mueveyManda(6))
			self.breporte.clicked.connect(self.enviarReporte)
			self.breporte.setShortcut('F7')
			self.bpanelconf.setShortcut('F7')
			self.bayuda.clicked.connect(lambda:self.mueveyManda(8))
			self.bcancelarPago.clicked.connect(self.cancelandoPago)
			self.bnoserie.clicked.connect(self.mostrarNoSerie)
			#self.bcam.clicked.connect(self.activaCamara)


			self.bentrar.clicked.connect(self.validaLogin)
			self.bboletoPerdido.clicked.connect(self.boletoPerdido)
			self.reporteTar.clicked.connect(self.imprimeReporteTarifas)
			self.bayudaCliente.clicked.connect(self.ayudando2)
			self.bayudaCliente2.clicked.connect(self.ayudando)

			self.bimprimeEventos.clicked.connect(self.imprimeReporteEventos)
			self.bpdf.clicked.connect(self.imprimeReporteEventosPDF)
			self.bimpReporteCaja.clicked.connect(self.imprimeReporte)
			self.secuenciaCobro(1)



			self.tablatarifas.setColumnCount(12)
			self.tablatarifas.setHorizontalHeaderLabels(['','Id','Prioridad','Fecha_ini','Fecha_fin','Hora_ini','Hora_fin','Dia_semana','Descripcion','costo','intervalo_1','intervalo_2'])

			self.tablaMantenimiento.setColumnCount(4)
			self.tablaMantenimiento.setHorizontalHeaderLabels(['Nombre','Tipo','Descripcion','Fecha y hora'])

			"""
			cur.execute("select MAX(\"idCajero\") from \"CAJERO\"")
			for reg in cur:
				idc=reg[0]

			cur.execute("update \"CAJERO\" set \"idCajero\"="+NoCajero+" where \"idCajero\"="+str(idc))
			"""
			conn.commit()



	################MODS########
			self.bapagar.clicked.connect(self.apagarRasp)
			self.breiniciar.clicked.connect(self.reiniciarRasp)
			self.bconfirmarIP.clicked.connect(self.cambiaIp)
			self.bpanelconf.clicked.connect(self.muestraPanel)
			self.bsalirConfig.clicked.connect(lambda:self.secuenciaCobro(1))
			self.bsalirLogin.clicked.connect(lambda:self.secuenciaCobro(1))
			self.bsalirsucursal.clicked.connect(lambda:self.cambia(17))
			self.bsalirred.clicked.connect(lambda:self.cambia(17))
			self.bsalirCambiarFecha.clicked.connect(lambda:self.cambia(17))
			self.bsucursal.clicked.connect(lambda:self.cambia(16))
			self.bred.clicked.connect(lambda:self.cambia(15))
			self.breporte.clicked.connect(lambda:self.secuenciaCobro(1))
			self.bhora.clicked.connect(lambda:self.cambia(19))
			
			self.lerror1.setVisible(False)
			self.bentrar.clicked.connect(self.validaLogin)
			self.bcambiarFecha.clicked.connect(self.cambiaFecha)
			#self.bguardar.clicked.connect(self.setConfig)
			#self.bsalirConfig.clicked.connect(self.salirConf)
			self.bconfirmarplaza.clicked.connect(self.setConfig)
			self.bcam.clicked.connect(self.scan)
			#self.bcam.setShortcut("Return")
			self.lscan.textChanged.connect(self.validacionScan)
			self.btest.clicked.connect(self.testTicket)
			self.btest.setShortcut("F3")
			self.bfueraServicio.clicked.connect(lambda:self.cambia(14))
			self.bfueraServicio.setShortcut("F4")
			self.bautomatizando.clicked.connect(lambda:self.cambia(21))
			self.bautomatizando.setShortcut("F5")
			self.bpagaralsalir.clicked.connect(lambda:self.cambia(20))
			self.bpagaralsalir.setShortcut("F6")
			self.binicio.clicked.connect(lambda:self.cambia(0))
			self.binicio2.clicked.connect(lambda:self.cambia(0))
			self.binicio3.clicked.connect(lambda:self.cambia(0))
			self.binicio4.clicked.connect(lambda:self.cambia(0))
			self.binicio.setShortcut("F1")
			self.binicio2.setShortcut("F1")
			self.binicio3.setShortcut("F1")
			self.binicio4.setShortcut("F1")

			##### Correccion cambio faltante ---------------
			self.PANTALLA_CAMBIO_FALTANTE = 22

			#####--------------Modo operacion------------
			self.boperacion.clicked.connect(lambda:self.cambia(23))
			self.bconfirmaroperacion.clicked.connect(self.establecerOperacion)
			self.bsaliroperacion.clicked.connect(lambda:self.cambia(0))
			#####--------------Modo operacion------------
			#####--------------Modo Recarga------------
			self.brecarga.clicked.connect(self.operacionRecarga)
			self.bconfirmarrecarga.clicked.connect(self.confirmarRecarga)
			self.bvaciar.clicked.connect(lambda:self.cambia(25))
			self.bvaciarsi.clicked.connect(self.vaciarCartucho)
			self.bvaciarno.clicked.connect(lambda:self.cambia(24))
			#####--------------Modo operacion------------
			#Creando respaldo de archivo de confguracion
			self.vizualizar = viewData('configuracion.ini')
			#self.vizualizar.getInfo()
			self.panelConfig()
			self.datosEstacionamiento()
			shutil.copy(ruta+"configParser/configuracion.ini", ruta+"configParser/configuracion_respaldo.ini")
			shutil.copy(ruta+"configParser/sensores.ini", ruta+"configParser/sensores_respaldo.ini")

			'''
			#####--------------Modo operacion------------
			self.listaDeVariables = ListaDeVariables()
			#---------------------------------------- Tarjeta de interfaz arduino
			self.controladora = self.establecerControladora(self.listaDeVariables)
			#self.obtenerConfiguracion()
			#self.establecerConfiguracion()
			#exit(0)
			'''
			
			#sensores.getInfo()
			#sensores.editValue('MONEDERO','moneda_1',str(1))
			
			
		def operacionRecarga(self):
			global secuencia_recarga
			secuencia_recarga = 1
			self.secuenciaCobro(4)


		def confirmarRecarga(self):
			global secuencia_recarga
			secuencia_recarga = 0
			self.cambia(0)


			
		def vaciarCartucho(self):
			sensores.editValue('MONEDERO','moneda_1',str(0))
			sensores.editValue('MONEDERO','moneda_2',str(0))
			sensores.editValue('MONEDERO','moneda_3',str(0))
			sensores.editValue('MONEDERO','moneda_4',str(0))
			self.cambia(24)

		def establecerControladora(self,listaDeVariables):
			global tipo_controladora
			if tipo_controladora == 0 :
				controladora = Controladora(listaDeVariables, tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO)
			if tipo_controladora == 1 :
				controladora = Controladora(listaDeVariables, tarjeta = Controladora.TARJETA_DE_PULSO)
			if tipo_controladora == 2 :
				controladora = Controladora(listaDeVariables, tarjeta = Controladora.TARJETA_DE_INTERFAZ_BLANCA)
			if tipo_controladora == 3 :
				controladora = Controladora(listaDeVariables, tarjeta = Controladora.TARJETA_DE_INTERFAZ_ARDUINO)
				
			return controladora

		def enviarReporte(self):
			global usuario
			print("Enviando reportes")
			self.secuenciaCobro(1)
			os.system("su "+usuario+" -c "+ruta+"../Reportes/run.sh")
			#os.system(ruta+"../Reportes/run.sh")



		def establecerOperacion(self):
			global encriptacion,tipo_controladora
			self.cambia(0)
			tipo_controladora = self.ccontroladora.currentIndex()
			encriptacion = self.cencriptacion.currentIndex()
			if(tipo_controladora == 0):
				print("Controladora arduino seleccionada")
				pass
			if(tipo_controladora == 1):
				print("Controladora pulso seleccionada")
				pass
			if(tipo_controladora == 2):
				print("Controladora raspberry seleccionada")
				pass
			if encriptacion == 0:
				print("Encriptacion desactivada")
			if encriptacion == 1:
				print("Encriptacion activada")


			self.vizualizar.editValue('CONTROLADORA','tipo_tc',str(tipo_controladora))
			self.vizualizar.editValue('GENERAL','encriptacion',str(encriptacion))
			
			
		"""	
		def scan(self):
			global mensajeBoletoUsado
			#thread3 = Thread(target=leerCodQR, args = ())
			text=self.lscan.text()
			codigo=text[0:1]
			print(codigo)
			if(codigo == 'M' or codigo == 'L'):
				text=text.replace("'","-")
				text=text.replace("Ñ",":")
				text=text.split(',')
				#os.system("sudo nice -n -19 python3 archimp.py")
				try:
					
					leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
					leerArch.write(str(text[0])+"\n"+str(text[1])+"\n"+str(text[2])+"\n"+str(text[3])+"\n"+str(text[4]))
					leerArch.close()
					self.lscan.setText('')
				except Exception as e:
					print(e)
					pass
				print('boleto valido')

			else:
				mensajeBoletoUsado = 1
				self.lscan.setText('')
				print('boleto invalido')
		"""
		def obtenerConfiguracion(self):
			global equipo, sucursal, tipo
			try:
				infile = open(rutaUsuario+"eum.conf", 'r')
				c=infile.readline()
				print(rutaUsuario,c)
				arr=c.split(',')
				equipo=int(arr[0])
				sucursal=int(arr[1])
				tipo=int(arr[2])
				infile.close()
				print("Configuracion encontrada: ",equipo,sucursal,tipo)
			except:
				print("Configuracion no encontrada ")
				equipo=1
				sucursal=1
				tipo=0
				infile = open(rutaUsuario+"eum.conf", "w")
				infile. write(str(equipo)+","+str(sucursal)+","+str(tipo))
				infile. close()
		
		def secuenciaSuspension(self,estado, cambio_faltante):
			#thread3 = Thread(target=leerCodQR, args = ())
			if estado == 1:
				if cambio_faltante: 
					print("Secuencia de suspension, cambio_faltante:",cambio_faltante)
					self.cambia(self.PANTALLA_CAMBIO_FALTANTE)
					self.lcambioFaltante.setText(str(cambio_faltante))
					return not estado
				else:
					self.cambia(14)
					return not estado
			else:
				self.cambia(0)
				return not estado

		def secuenciaCobro(self,secuencia):
			#thread3 = Thread(target=leerCodQR, args = ())
			if(secuencia == 0):
				#self.cambia(0)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,0,1,0,2,0])
				ser.write(a);
			if(secuencia == 1):
				self.cambia(0)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,1,1,0,2,0])
				#ser.write(a);
			if(secuencia == 2):
				self.cambia(1)
				#self.cambia(24)

				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,0,1,1,2,0])
				#ser.write(a);
			if(secuencia == 3):
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,0,1,0,2,1])
				#ser.write(a);

			#Secuencia de recarga	
			if(secuencia == 4):
				self.cambia(24)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.LED, [0,0,1,1,2,0])


		def testTicket(self):
			#thread3 = Thread(target=leerCodQR, args = ())
			aux_tarifa = 200
			self.lscan.setText("M,60,1,21'06'2019,10Ñ30Ñ12.")
			self.scan("M,60,1,21'06'2019,10Ñ30Ñ12.")

		def validacionScan(self):
			#thread3 = Thread(target=leerCodQR, args = ())
			global encriptacion
			text=self.lscan.text()
			print(text)
			inicioChar=text[:1]
			
			if inicioChar == "L":
					if len(text) == 9:
						self.scan2()
						
			if "." in text:

				'''DL17'''
				if encriptacion:
					dencriptador = codificar()
					text = str(dencriptador.procesamiento(text))
					print("Desencriptar ************************************************",text)
					if text == "0":
						self.mensajeError = 1
					if text == "-1":
						self.mensajeError = 1

				else:
					text = str(text)
					print("Des ************************************************",text)
				'''DL17'''

				inicioChar=text[:1]
				if inicioChar == "M":
					#text = text[1:-1:]
					self.scan(text)
				else:
					self.lscan.setText('')
			
			#text2char=text[:2]
			#scan()


		def scan2(self):
			global Boleto,mensajeError
			#thread3 = Thread(target=leerCodQR, args = ())
			text=self.lscan.text()
			
			text2char=text[:2]
			if('M,' == text2char or 'L,' == text2char):
				if 'M,' == text2char:
					text = text[0:-1:]   #Retira caracteres de inicio y de fin
				text=text.replace("'","-")
				text=text.replace("Ñ",":")
				text=text.split(',')
				#os.system("sudo nice -n -19 python3 archimp.py")
				#os.system("sudo nice -n -19 python3 archimp.py")
				try:
					#leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
					#leerArch.write(str(text[0])+"\n"+str(text[1])+"\n"+str(text[2])+"\n"+str(text[3])+"\n"+str(text[4])[:8])
					#leerArch.close()
					Boleto = text
					print(Boleto,'...Boleto')
					self.lscan.setText('')
				except Exception as e:
					print(e,'datetime incorrecto')
					self.lscan.setText('')
					mensajeError = 1
					pass
			else:
				mensajeError = 1
				self.lscan.setText('')
				print('boleto invalido',text,text2char)

		def scan(self,text):
			#thread3 = Thread(target=leerCodQR, args = ())
			global mensajeError,Boleto
			#text=self.lscan.text()
			try:
				text2char=text[:2]
				if('M,' == text2char or 'L,' == text2char):
					if 'M,' == text2char:
						text = text[0:-1:]   #Retira caracteres de inicio y de fin
					text=text.replace("'","-")
					text=text.replace("Ñ",":")
					text=text.split(',')
					#os.system("sudo nice -n -19 python3 archimp.py")
					#os.system("sudo nice -n -19 python3 archimp.py")
					text[1]= int(text[1])
					text[2] = int(text[2])
					print(str(text[3])+" "+str(text[4]),'datetime...')
					fecha = datetime.strptime(str(text[3])+" "+str(text[4]), '%d-%m-%Y %H:%M:%S')
					#leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
					#leerArch.write(str(text[0])+"\n"+str(text[1])+"\n"+str(text[2])+"\n"+str(text[3])+"\n"+str(text[4])[:8])
					#leerArch.close()
					Boleto = text
					print(Boleto,'...Boleto')
					self.lscan.setText('')
				else:
					mensajeError = 1
					self.lscan.setText('')
					print('boleto invalido',text,text2char)
			except Exception as e:
				print(e,'Error en la lectura del boleto')
				self.lscan.setText('')
				mensajeError = 1
				pass
		
		def validaLogin(self):
			global cur,accesoAcaja,USUARIO,correoUSUARIO,user,pswd
			nom=self.lusu.text()
			rol_us=""
			indice=0
			contr=self.lcont.text()
			if(nom=="eum"):
				if(contr=="pi"):
					self.cambia(18)
				else:
					self.lerror1.setText("usuario o contraseña incorrectos")
					self.lerror1.setVisible(True)
			else:
				self.lerror1.setText("usuario o contraseña incorrectos")
				self.lerror1.setVisible(True)
			"""cur.execute("SELECT * FROM \"USUARIO\" WHERE usuario=%s and contra=%s order by \"idUsuario\" ASC",(nom,contr))

			print("nom,contr=",nom,contr)
			for reg in cur:
				print(reg[1],reg[2],reg[3],reg[4],reg[5],reg[6])
				rol_us=reg[1]
				indice=1
			if(indice==0):
				self.lerror1.setText("usuario o contraseña incorrectos")
				self.lerror1.setVisible(True)
			else:
				USUARIO=str(reg[0])
				self.cambia(5)"""
		
		def cambiaFecha(self):
			a=self.dtime.dateTime()
			b=self.dtime.textFromDateTime(a)
			print(b,type(b))
			os.system("sudo date -s '"+b+"' ")
			
		
		def setConfig(self):
			global plaza,localidad,equipo,host,ip,pol,pol1,pol2,pol3,pol4,pol5,impresora,anchoPapel,tipo_controladora,encriptacion
			lenn=0
			plaza=str(self.lnom.text())
			localidad=str(self.lloc.text())
			equipo=str(self.leq.text())
			
			
			print(plaza,localidad)
			dat=plaza+","+localidad+","+str(equipo)
			infile = open(ruta+"archivos_config/datos.txt", 'w')
			c=infile.write(dat)

			self.datosEstacionamiento()
			self.secuenciaCobro(1)
			
		'''
		def setConfig(self):
			global plaza,localidad,noEquipo,pol,pol1,pol2,pol3,pol4,pol5,impresora,anchoPapel
			lenn=0
			plaza=str(self.lnom.text())
			localidad=str(self.lloc.text())
			noEquipo=str(self.leq.text())
			
			self.vizualizar.editValue('GENERAL','nombre_sucursal',plaza)
			self.vizualizar.editValue('GENERAL','localidad_sucursal',localidad)
			self.vizualizar.editValue('GENERAL','id',str(noEquipo))

			

			self.datosEstacionamiento()
			self.secuenciaCobro(1)
			
		'''
			
			
			
			
		def datosEstacionamiento(self):
			global plaza,localidad,equipo,host,ip,pol,pol1,pol2,pol3,pol4,pol5,impresora,anchoPapel,tipo_controladora,encriptacion
			lenn=0
			self.lnom.setText(plaza)
			self.lloc.setText(localidad)
			self.leq.setText(str(equipo))
			self.nomPlaza_2.setText(plaza)
			self.nomLoc_2.setText(localidad)
			self.lhost.setText(host)
			self.lip.setText(ip)
			self.lid.setText(str(equipo))
			self.ccontroladora.setCurrentIndex(tipo_controladora)
			self.cencriptacion.setCurrentIndex(encriptacion)
			

			
		
		def panelConfig(self):
			global plaza,localidad,equipo,host,ip,tipo_controladora,encriptacion
			infile = open(ruta+'archivos_config/datos.txt','r')
			datos= infile.readline()
			arr=datos.split(',')
			plaza=arr[0]
			localidad=arr[1]
			equipo=arr[2]
			infile.close()
			
			infile = open(ruta+'archivos_config/red.txt','r')
			datos= infile.readline()
			arr=datos.split(',')
			host=arr[0]
			ip=arr[1]
			infile.close()
			
			tipo_controladora = int(self.vizualizar.getValue('CONTROLADORA','tipo_tc'))
			encriptacion = int(self.vizualizar.getValue('GENERAL','encriptacion'))
			
		'''	
		def panelConfig(self):
			global plaza,localidad,equipo,host,ip,tipo_controladora,encriptacion
			panelConf=1

			#self.vizualizar = viewData()
			self.vizualizar.getInfo()


			tipo_controladora = int(self.vizualizar.getValue('CONTROLADORA','tipo_tc'))
			encriptacion = int(self.vizualizar.getValue('GENERAL','encriptacion'))
			plaza = self.vizualizar.getValue('GENERAL','nombre_sucursal')
			localidad = self.vizualizar.getValue('GENERAL','localidad_sucursal')
			host = self.vizualizar.getValue('RED','server_ip_address')
			ip = self.vizualizar.getValue('RED','ip_addeess')
			noEquipo = int(self.vizualizar.getValue('GENERAL','id'))
			sucursal_id = int(self.vizualizar.getValue('GENERAL','id_sucursal'))
			pol = self.vizualizar.getValue('GENERAL','politicas')
			impresora = int(self.vizualizar.getValue('EXPEDIDORA','modelo_impresora'))
			anchoPapel = int(self.vizualizar.getValue('EXPEDIDORA','ancho_papel'))
			sensor = int(self.vizualizar.getValue('EXPEDIDORA','sensor'))
			segundos = int(self.vizualizar.getValue('EXPEDIDORA','segundos'))
			pol1 = self.vizualizar.getValue('EXPEDIDORA','parrafo_1')
			pol2 = self.vizualizar.getValue('EXPEDIDORA','parrafo_2')
			pol3 = self.vizualizar.getValue('EXPEDIDORA','parrafo_3')
			pol4 = self.vizualizar.getValue('EXPEDIDORA','parrafo_4')
			pol5 = self.vizualizar.getValue('EXPEDIDORA','parrafo_5')


		'''
		def salirConf(self):
			global panelConf
			panelConf=0
			self.secuenciaCobro(1)
			

		
		
		
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
				
				
		def cambiaIp(self):
			global host,ip
			host=self.lhost.text()
			ip=self.lip.text()

			self.sustituye(ruta+"cliente.py","192.168","host = '"+host+"'")
			self.sustituye("/etc/dhcpcd.conf","ip_address","static ip_address="+ip+"/24")
			ip=ip.split(".")
			ip=ip[0]+"."+ip[1]+"."+ip[2]+".1"
			self.sustituye("/etc/dhcpcd.conf","routers","static routers="+ip)

			
			host=str(self.lhost.text())
			ip=str(self.lip.text())
			
			
			print(plaza,localidad)
			dat=host+","+ip
			infile = open(ruta+"archivos_config/red.txt", 'w')
			c=infile.write(dat)
			
			self.datosEstacionamiento()
			self.secuenciaCobro(1)
			
			
		def muestraPanel(self):
			self.cambia(17)
			#datos=obtenerPlazaYLocalidad()
			#self.lno.setText(str(datos[0]))
			#self.llo.setText(str(datos[1]))
			#datos=obtenerTerminal()
			self.lusu.setText('')
			self.lcont.setText('')
			self.lerror1.setText('')
			
		def cambia(self,val):
			self.stackedWidget.setCurrentIndex(val)
		
		def apagarRasp(self):
			print("apagando...")
			os.system("sudo shutdown -P 0")
		def reiniciarRasp(self):
			print("apagando...")
			os.system("sudo shutdown -r 0")
			############################MODS FIN#################

		def activaCamara(self):
			#thread3 = Thread(target=leerCodQR, args = ())
			thread3 = Thread(target=leerCodQR, args = ())
			#os.system("sudo nice -n -19 python3 archimp.py")
			try:
			
				thread3.start()



			except Exception as e:
				pass
			#p=subprocess.Popen(['/home/cajero/scanner/dsreader -l 1 -s 20 > /home/cajero/Documentos/ticket.txt'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
			
			#so=os.popen('~/bin/dsreader -l 1 -s 20 > /home/cajero/Documentos/ticket.txt')
			
			
		def mostrarNoSerie(self):
			global accesoAcaja,NoCajero,mensajeAyuda
			os.system("sudo grep Serial /proc/cpuinfo >> /home/cajero/Escritorio/numeroSerial.txt")
			configuracion=[]
			archivo=open(PATH_ARCHIVO_CONFIGURACION_TERMINAL_SERIAL, "r")
			c=archivo.readline()
			serie=c.split(':', 1 )
			archivo.close()
			self.lserie.setText("No. Serie: "+str(serie[1]))

			self.lmodelo.setVisible(True)
			self.lserie.setVisible(True)

		def ayudando(self):
			global accesoAcaja,NoCajero,mensajeAyuda
			descripciones=self.obtenerDineroActual()
			mensaje=str("ayuda@ayuda.com")+","+str(NoCajero)+",3,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)

			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				#botones.apagarMonedero()
				mensajeAyuda=1
				pass

		def ayudando2(self):
			global accesoAcaja,NoCajero,mensajeAyuda
			descripciones=self.obtenerDineroActual()
			mensaje=str("ayuda@ayuda.com")+","+str(NoCajero)+",3,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)

			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				#botones.apagarMonedero()
				mensajeAyuda=1
				self.aviso1.setText("Tu peticion esta siendo atendida")
				pass

		def cancelandoPago(self):
			global cp
			print("BOTON CANCEL PRESIONADO")
			cp=1

		def finalizarCalibracion(self):
			global cartuchoRemovido,NoCajero,correoUSUARIO,cajeroSuspendido
			cajeroSuspendido=0
			if(cartuchoRemovido==0):
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",1"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
			else:
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass

		def finalizarCorteCaja(self):
			global cartuchoRemovido,NoCajero,correoUSUARIO
			if(cartuchoRemovido==0):
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",1"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
			else:
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
				#no sabria que hacer

		def finalizarSoporteTecnico(self):
			global cartuchoRemovido,NoCajero,correoUSUARIO
			if(cartuchoRemovido==0):
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",1"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
			else:
				cartuchoRemovido=0
				self.cambia(9)
				mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2"
				resultado=Servidor.configSocket("log final", mensaje)
				if(resultado==-1):
					pass
				else:
					pass
				#no sabria que hacer

		def imprimeReporteEventosPDF(self):
			dia=str(self.fechaInicio.date().day())
			mes=str(self.fechaInicio.date().month())
			anio=str(self.fechaInicio.date().year())

			dia2=str(self.fechaFin.date().day())
			mes2=str(self.fechaFin.date().month())
			anio2=str(self.fechaFin.date().year())

			fecha1=dia+"/"+mes+"/"+anio+" 00:00:00"
			fecha2=dia2+"/"+mes2+"/"+anio2+" 23:59:59"
			fechaFinal=fecha1+","+fecha2
			leerArch = open(rutaUsuario+"Documentos/fechaEventos.txt", "a+")
			leerArch.write(fechaFinal)
			leerArch.close()
			os.system("sudo python3 "+ruta+"reporteEventosPDF.py")

		def imprimeReporteEventos(self):
			dia=str(self.fechaInicio.date().day())
			mes=str(self.fechaInicio.date().month())
			anio=str(self.fechaInicio.date().year())

			dia2=str(self.fechaFin.date().day())
			mes2=str(self.fechaFin.date().month())
			anio2=str(self.fechaFin.date().year())

			fecha1=dia+"/"+mes+"/"+anio+" 00:00:00"
			fecha2=dia2+"/"+mes2+"/"+anio2+" 23:59:59"
			fechaFinal=fecha1+","+fecha2
			leerArch = open(rutaUsuario+"Documentos/fechaEventos.txt", "a+")
			leerArch.write(fechaFinal)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/cajero/reporteEventos.py")

		def imprimeReporteTarifas(self):
			dia=str(self.fechaInicio2.date().day())
			mes=str(self.fechaInicio2.date().month())
			anio=str(self.fechaInicio2.date().year())

			dia2=str(self.fechaFin2.date().day())
			mes2=str(self.fechaFin2.date().month())
			anio2=str(self.fechaFin2.date().year())

			fecha1=dia+"/"+mes+"/"+anio+" 00:00:00"
			fecha2=dia2+"/"+mes2+"/"+anio2+" 23:59:59"
			fechaFinal=fecha1+","+fecha2
			leerArch = open(rutaUsuario+"Documentos/fechaTarifas.txt", "a+")
			leerArch.write(fechaFinal)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/cajero/reporteTarifas.py")


		def leerBotones(self):
			global cp,leido,opcionAdmin,accesoAcaja,NoCajero,accesoAcaja,aux_tarifa,cambio
			#botones.configurarPinesGPIO()
			#botones.prenderMonedero()
			#chapaMagnetica = botones.leerBotonesEntrada()
			#bnCancelar = botones.botonCancelar()
			#chapaMagnetica2=botones.leerBotonesEntrada2()
			#if(bnCancelar):
			#if(bnCancelar and aux_tarifa!=0):
			#	cp=1
			#	print("BOTON CANCELAR PRESIONADOO")

			botonAsistencia = 0
			ser.limpiar()
			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
			ser.write(a);
			time.sleep(.001)	

			r = ser.read(6)
			if (r):
				print ("BOTON", r, r[0], ord(Comunicacion.caracterDeInicio))

				if len(r) == 6:
					if r[0] == ord(Comunicacion.caracterDeInicio):
						if r[5] == ord(Comunicacion.caracterDeFin):
							#print ("Boton", r[1])

							botonAsistencia = (r[1]) & 1



			if botonAsistencia == 1:
				print("Pidiendo asistencia")
				os.system(ruta+"/Asistencia/asistencia.sh")


			"""
			if(chapaMagnetica==True):
				print("Magnetizado")
				if(chapaMagnetica2==True):
					print("cerrado y magnetizado")
				else:
					print("abierto y magnetizado")
					if(accesoAcaja=1):
						#Mostrar mensaje en pantalla... Cerrar puerta!!!  , ALERTA
					else:
						#ALERTA: CAJERO ABIERTO SIN AUTORIZACION
						mensaje=str("ASALTO@ayuda.com")+","+str(NoCajero)+",4,"+"0:0"+","+"0:0"
						resultado=Servidor.configSocket("log inicial", mensaje)
						if(resultado==-1):
							self.lerror1.setText("Problema en la conexion")
							self.lerror1.setVisible(True)
						else:
							pass
			else:
				if(chapaMagnetica2==True):
					print("cerrado y DESmagnetizado")
					#Sin significado, NO ACCION.
				else:
					print("abierto y DESmagnetizado")
					#Se esta retirando el dinero posiblemente... 10 segeundos limite para magnetizar....
			if(sensorMovimiento==True):
				print("OK")
			else:
				if(opcionAdmin==2):
					print("OK2")
				else:
					print("Caja levantada")
					descripciones=self.obtenerDineroActual()
					mensaje=str("sensorCaja@ayuda.com")+","+str(NoCajero)+",4,"+"0:0"+","+"0:0"
					resultado=Servidor.configSocket("log inicial", mensaje)
					if(resultado==-1):
						self.lerror1.setText("Problema en la conexion")
						self.lerror1.setVisible(True)
					else:
						pass
				
			"""
				#self.avisoInserta.setText("Puerta cerrada")
			QtCore.QTimer.singleShot(100, self.leerBotones)

		def imprimeReporte(self):
			global contadorCartuchos
			fec=datetime.now().date()
			fec=str(fec.day)+"/"+str(fec.month)+"/"+str(fec.year)
			k1=self.m1.text()
			k2=self.m2.text()
			k3=self.m5.text()
			k4=self.m10.text()
			k5=self.mt.text()
			k6=self.b20.text()
			k7=self.b50.text()
			k8=self.b100.text()
			k9=self.b200.text()
			k10=self.bt.text()
			k11=self.dm.text()
			k12=self.db.text()
			k13=self.dt.text()
			datos=fec+','+k1+','+k2+','+k3+','+k4+','+k5+','+k6+','+k7+','+k8+','+k9+','+k10+','+k11+','+k12+','+k13+','+str(contadorCartuchos)
			leerArch = open(rutaUsuario+"Documentos/reporteCorteCaja.txt", "a+")
			leerArch.write(datos)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/cajero/imprimeCorte.py")
		def mueveyManda(self,valor):
			global opcionAdmin
			opcionAdmin=valor
			self.cambia(11)
			self.lerror1.setVisible(False)
			self.lusu.setText("")
			self.lcont.setText("")

		


		def calibrando(self):
			global contadorCartuchos,monedas,monedasTotal,dineroTotal,correoUSUARIO,accesoAcaja,NoCajero
			fecha=hora.mostrarFechayHora()
			i=-1
			descripciones=self.obtenerDineroActual()
			mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)
			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				fecha=hora.mostrarFechayHora()
				accesoAcaja=1
				botones.abrirPuerta()
				contadorCartuchos=contadorCartuchos+1
				self.lnumc.setText(str(contadorCartuchos))
				self.lniv.setText(""+str(nivelActual[0])+","+str(nivelActual[1])+","+str(nivelActual[2])+","+str(nivelActual[3]))
				self.cambia(5)
				monedas[0]=monedas[0]+85
				monedas[1]=monedas[1]+78
				monedas[2]=monedas[2]+69
				monedas[3]=monedas[3]+58
				monedasTotal=monedasTotal+290
				dineroTotal=dineroTotal+1166

				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",5,'"+str(contadorCartuchos)+"','"+fecha+"')"
				cur.execute(consu)
				conn.commit()

			#REPORTAR LOG A SERVIDOR....

		def menuPublicidad(self):
			global USUARIO,accesoAcaja
			fecha=hora.mostrarFechayHora()
			accesoAcaja=1
			botones.abrirPuerta()
			botones.configurarPublicidad()
			botones.manteniendoElCero()
			consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",8,'Publicidad','"+fecha+"')"
			cur.execute(consu)
			conn.commit()

		def reemplazoPapel(self):
			global correoUSUARIO,accesoAcaja,NoCajero
			descripciones=self.obtenerDineroActual()
			mensaje=str(correoUSUARIO)+","+str(NoCajero)+",2,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)
			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				fecha=hora.mostrarFechayHora()
				accesoAcaja=1
				botones.abrirPuerta()
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",9,'rollo reemplazado','"+fecha+"')"
				cur.execute(consu)
				conn.commit()

		def seccionAyuda(self):
			global correoUSUARIO,accesoAcaja,NoCajero
			descripciones=self.obtenerDineroActual()
			mensaje=str(correoUSUARIO)+","+str(NoCajero)+",3,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)
			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				fecha=hora.mostrarFechayHora()
				accesoAcaja=1
				botones.abrirPuerta()
				self.cambia(4)
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",9,'rollo reemplazado','"+fecha+"')"
				cur.execute(consu)
				conn.commit()

		def llenaCamposPlaza(self):
			global rep,nom,loc,nivelDeCambio
			infile = open(rutaUsuario+"Documentos/plaza.txt", 'r')
			c=infile.readline()
			arr=c.split(',', 1 )
			infile.close()
			nom=str(arr[0])
			loc=str(arr[1])
			self.lnom.setText(nom)
			self.llol.setText(loc)
			self.cambia(10)
		
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
		

		def cambiaNombre(self):
			global nom,loc,USUARIO
			fecha=hora.mostrarFechayHora()
			outfile = open(rutaUsuario+"Documentos/plaza.txt", 'w')
			nn=self.lnom.text()
			ln=self.llol.text()
			outfile.write(str(nn)+","+str(ln))
			outfile.close()
			
			nocaj=self.lcaj.text()
			
			outfile = open(rutaUsuario+"Documentos/NoCajero.txt", 'w')
			outfile.write(str(nocaj))
			outfile.close()
			host=self.lhost.text()
			ip=self.lip.text()
			
			self.sustituye(ruta+"cliente.py","192.168","	host = '"+host+"'")
			self.sustituye("/etc/dhcpcd.conf","ip_address","static ip_address="+ip+"/24")
			ip=ip.split(".")
			ip=ip[0]+"."+ip[1]+"."+ip[2]+".1"
			self.sustituye("/etc/dhcpcd.conf","routers","static routers="+ip)
			
			nom=self.lnom.text()
			loc=self.llol.text()
			self.cambia(9)
			consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",6,'"+str(nn)+","+str(ln)+"','"+fecha+"')"
			cur.execute(consu)
			conn.commit()


		def holi(self,val):
			print(val)
			if(val==3):
				self.lnom.setText("hola")
				self.llol.setText("")
			if(val==6):
				self.llol.setText("hola")
				self.lnom.setText("")


		def tecladoSum(self,val):
			if(val==10):
				self.valvol.setText("$")
			else:
				self.valvol.setText(self.valvol.text()+str(val))


		def volConfirmado(self):
			global aux_tarifa,cambio,aportacionConfirmada
			aportacionConfirmada=1
			if(self.valvol.text()=="$" or self.valvol.text()=="$0"):
				aux_tarifa=0
				#cambio=0
			else:
				valPropuesto=self.valvol.text()[1:]
				print("valvol: ",valPropuesto)
				aux_tarifa=int(self.valvol.text()[1:])
			self.secuenciaCobro(2)
			"""if(valPropuesto!=0):
				print("ACA")
				self.alerta.setVisible(True)
			else:
				print("ALLA")
				aux_tarifa=int(self.valvol.text()[1:])
				self.secuenciaCobro(2)"""







		def actualizaMensaje2(self):
			global cur
			vac=2
			idt=self.idtar1.value()
			cur.execute("select estado from \"TARIFA\" where \"idTarifa\"="+str(idt))
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

		def actualizaMensaje(self):
			global cur
			vac=2
			idt=self.idtar2.value()
			cur.execute("select estado from \"TARIFA\" where \"idTarifa\"="+str(idt))
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



		def habilitaTarifa(self):
			global cur,conn,USUARIO
			idt=self.idtar2.value()
			fecha=hora.mostrarFechayHora()
			vac=0
			cur.execute("select estado from \"TARIFA\" where \"idTarifa\"="+str(idt))
			for reg in cur:
				vac=reg[0]
				print(reg[0])

			if(vac==0):

				cur.execute("update \"TARIFA\" set estado=1 where \"idTarifa\"="+str(idt))
				self.bhabilitar.setText("Deshabilitar")
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",1,'"+str(idt)+"','"+fecha+"')"
				cur.execute(consu)
				conn.commit()
			else:
				cur.execute("update \"TARIFA\" set estado=0 where \"idTarifa\"="+str(idt))
				self.bhabilitar.setText("Habilitar")
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",2,'"+str(idt)+"','"+fecha+"')"
				cur.execute(consu)
				conn.commit()


			self.llenaTabla()


		def seccionTarifas(self):
			global cur
			self.cambia(6)
			self.llenaTabla()

		def llenaTabla(self):
			global cur
			cur.execute("select * from \"TARIFA\" order by prioridad Desc")
			rowc=self.tablatarifas.rowCount()
			k=0
			while(k<rowc):
				self.tablatarifas.removeRow(0)
				#del self.CB2[0]
				k=k+1
			row=0
			for reg in cur:
				#print(reg[0],reg[1],reg[2],reg[3],reg[4],reg[5],reg[6],reg[7],reg[8],reg[9],reg[10],reg[11])
				self.tablatarifas.insertRow(row)
				idt=QTableWidgetItem(str(reg[0]))
				pri=QTableWidgetItem(str(reg[12]))
				fi=QTableWidgetItem(str(reg[2]))
				ff=QTableWidgetItem(str(reg[3]))
				hi=QTableWidgetItem(str(reg[4]))
				hf=QTableWidgetItem(str(reg[5]))
				ds=QTableWidgetItem(str(reg[6]))
				des=QTableWidgetItem(str(reg[7]))
				cos=QTableWidgetItem(str(reg[8]))
				i1=QTableWidgetItem(str(reg[9]))
				i2=QTableWidgetItem(str(reg[10]))
				if(reg[11]==1):
					state=QTableWidgetItem("Habilitada")
				else:
					state=QTableWidgetItem("Deshabilitada")
				self.tablatarifas.setItem(row,0,state)
				self.tablatarifas.item(row,0).setTextAlignment(4)

				self.tablatarifas.setItem(row,1,idt)
				self.tablatarifas.item(row,1).setTextAlignment(4)
				self.tablatarifas.setItem(row,2,pri)
				self.tablatarifas.item(row,2).setTextAlignment(4)
				self.tablatarifas.setItem(row,3,fi)
				self.tablatarifas.item(row,3).setTextAlignment(4)
				self.tablatarifas.setItem(row,4,ff)
				self.tablatarifas.item(row,4).setTextAlignment(4)
				self.tablatarifas.setItem(row,5,hi)
				self.tablatarifas.item(row,5).setTextAlignment(4)
				self.tablatarifas.setItem(row,6,hf)
				self.tablatarifas.item(row,6).setTextAlignment(4)
				self.tablatarifas.setItem(row,7,ds)
				self.tablatarifas.item(row,7).setTextAlignment(4)
				self.tablatarifas.setItem(row,8,des)
				self.tablatarifas.item(row,8).setTextAlignment(4)
				self.tablatarifas.setItem(row,9,cos)
				self.tablatarifas.item(row,9).setTextAlignment(4)
				self.tablatarifas.setItem(row,10,i1)
				self.tablatarifas.item(row,10).setTextAlignment(4)
				self.tablatarifas.setItem(row,11,i2)
				self.tablatarifas.item(row,11).setTextAlignment(4)
				row=row+1



		def elimina2(self):
			global cur,conn,USUARIO
			fecha=hora.mostrarFechayHora()
			idt=self.idtar1.value()
			print("Eliminado Caon")
			cur.execute("delete from \"TARIFA\" where \"idTarifa\"="+str(idt))
			consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",3,'"+str(idt)+"','"+fecha+"')"
			cur.execute(consu)
			conn.commit()
			self.llenaTabla()





		def tarifaConfirmada(self):
			global USUARIO
			fecha=hora.mostrarFechayHora()
			int1=""
			int2=""
			dia1=""
			mes1=""
			anio1=""
			dia2=""
			mes2=""
			anio2=""
			hora1=""
			minuto1=""
			hora2=""
			minuto2=""
			self.prioridad=0
			cons=""
			intok=""
			fecok=""
			horok=""
			dsemok=""
			costo=0
			dsem=""
			dsem2=""
			descr=""
			destar=""
			segundoIndicador=""

			print(cons)
			if(self.ch1.checkState()==2):
				self.prioridad=self.prioridad+1
				int1=","+str(self.i1.value())
				int2=","+str(self.i2.value())
				intok=",int_1,int_2"
				#segundoIndicador=segundoIndicador+"A"
			if(self.ch2.checkState()==2):
				self.prioridad=self.prioridad+1
				mes1=",'"+str(self.f1.date().month())
				dia1="/"+str(self.f1.date().day())
				anio1="/"+str(self.f1.date().year())
				mes2="','"+str(self.f2.date().month())
				dia2="/"+str(self.f2.date().day())
				anio2="/"+str(self.f2.date().year())+"'"
				fecok=",fec_ini,fec_fin"
				#segundoIndicador=segundoIndicador+"B"
			if(self.ch3.checkState()==2):
				self.prioridad=self.prioridad+1
				hora1=",'"+str(self.h1.time().hour())
				minuto1=":"+str(self.h1.time().minute())
				hora2="','"+str(self.h2.time().hour())
				minuto2=":"+str(self.h2.time().minute())+"'"
				horok=",hor_ini,hor_fin"
				#segundoIndicador=segundoIndicador+"C"
			if(self.ch4.checkState()==2):
				self.prioridad=self.prioridad+1
				dsem2=dsem2+",'"
				if(self.chlunes.checkState()==2):
					dsem=dsem+",lunes"
				if(self.chmartes.checkState()==2):
					dsem=dsem+",martes"
				if(self.chmiercoles.checkState()==2):
					dsem=dsem+",miercoles"
				if(self.chjueves.checkState()==2):
					dsem=dsem+",jueves"
				if(self.chviernes.checkState()==2):
					dsem=dsem+",viernes"
				if(self.chsabado.checkState()==2):
					dsem=dsem+",sabado"
				if(self.chdomingo.checkState()==2):
					dsem=dsem+",domingo"
				dsem=dsem.lstrip(",")
				dsem2=dsem2+dsem
				dsem2=dsem2+"'"
				#segundoIndicador=segundoIndicador+"D"





				dsem=dsem.rstrip(",")
				dsemok=",dia_sem"
				print(dsem)

			print(self.prioridad)

			#Determinando prioridad compuesta
			if(self.prioridad!=0):
				#self.prioridad=str(self.prioridad)+segundoIndicador+"'"
				self.prioridad=str(self.prioridad)+"'"
				cost=","+str(self.costo.value())
				descr=",'"+str(self.descripcion.toPlainText())+"'"
				archivo = open(rutaUsuario+"Documentos/NoCajero.txt", "r")
				idCajero=str(archivo.readline().rstrip("\n"))
				archivo.close()
				cur.execute("select * from \"CAJERO\" where \"idCajero\"=%s",(idCajero))
				for reg in cur:
					print(reg[0],reg[1])
				plaza=reg[1]


				cons="INSERT INTO \"TARIFA\" (prioridad,des_tar"+intok+fecok+horok+dsemok+",costo,estado,plaza) values ('"+str(self.prioridad)+descr+int1+int2+mes1+dia1+anio1+mes2+dia2+anio2+hora1+minuto1+hora2+minuto2+dsem2+cost+",1,"+str(plaza)+")"
				print("PK",cons)
				cur.execute(cons)
				conn.commit()

				cur.execute("select MAX(\"idTarifa\") from \"TARIFA\"")
				for reg in cur:
					idtar=reg[0]

				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",7,'"+str(idtar)+"','"+fecha+"')"
				cur.execute(consu)
				conn.commit()
				self.cambia(6)
				self.llenaTabla()


		def saliendoAdmin(self):
			global config
			self.secuenciaCobro(1)
			config=0
			self.lusu.setText('')
			self.lcont.setText('')
			fecha=hora.mostrarFechayHora()
			self.lmodelo.setVisible(False)
			self.lserie.setVisible(False)

		def obtenerDineroActual(self):
			global monedas,billetes
			descripcionMonedas=str(monedas[0])+":1;"+str(monedas[1])+":2;"+str(monedas[2])+":5;"+str(monedas[3])+":10"
			descripcionBilletes=str(billetes[0])+":20;"+str(billetes[1])+":50;"+str(billetes[2])+":100;"+str(billetes[3])+":200"
			return descripcionMonedas,descripcionBilletes

		def cortandoLaCaja(self):
			global accesoAcaja,correoUSUARIO,contadorCartuchos,monedas,monedasTotal,dineroTotal,dineroTotalB,billetesTotales,billetes,NoCajero
			fecha=hora.mostrarFechayHora()
			i=-1
			descripciones=self.obtenerDineroActual()
			mensaje=str(correoUSUARIO)+","+str(NoCajero)+",1,"+descripciones[0]+","+descripciones[1]
			resultado=Servidor.configSocket("log inicial", mensaje)
			if(resultado==-1):
				self.lerror1.setText("Problema en la conexion")
				self.lerror1.setVisible(True)
			else:
				accesoAcaja=1
				botones.abrirPuerta()
				self.cambia(3)
				botones.abrirPuerta()
				self.m1.setText(str(monedas[0]))
				self.m2.setText(str(monedas[1]))
				self.m5.setText(str(monedas[2]))
				self.m10.setText(str(monedas[3]))
				self.mt.setText(str(monedas[0]+monedas[1]+monedas[2]+monedas[3]))
				self.b20.setText(str(billetes[0]))
				self.b50.setText(str(billetes[1]))
				self.b100.setText(str(billetes[2]))
				self.b200.setText(str(billetes[3]))
				self.bt.setText(str(billetes[0]+billetes[1]+billetes[2]+billetes[3]))
				self.dm.setText(str(dineroTotal))
				self.db.setText(str(dineroTotalB))
				self.dt.setText(str(dineroTotal+dineroTotalB))
				self.imprimeReporte()
				consu="insert into \"USUARIO_LOG\"(usuario,log,detalle,fecha) values("+str(USUARIO)+",4,'CC','"+fecha+"')"
				cur.execute(consu)
				conn.commit()
				monedas=[85,78,69,58]
				monedasTotal=290
				dineroTotal=1166
				dineroTotalB=0
				billetesTotales=0
				billetes=[0,0,0,0]
				contadorCartuchos=1

		def generaReporte(self):
			global config
			self.secuenciaCobro(1)
			config=0

		def boletoPerdido(self):
			global mensajeBoletoPerdido
			mensajeBoletoPerdido=1

		def pollingConexion(self):
			global conexion_activa
			#conexion_activa = conexion.obtenerLogs()
			#print("conexion:",conexion_activa)
			try:
				#conexion_activa = conexion.pollConexion(0,str(tipo)+str(equipo))
				#conexion_activa = conexion.activo()
				conexion_activa = True
				print("conexion:",conexion_activa,tipo,equipo)
			except:
				traceback.print_exc()
				print("Error al enviar informacion de conexion.")

			QtCore.QTimer.singleShot(4000,self.pollingConexion)


		def logPrender(self):
			try:

				prendido = conexion.logPrendido()
				print("Se registro log de prendido")
			except:
				print("Error al registrar log de prendido")


		def montos(self):
			global secuencia_recarga,FALTANTE,CobroFinalizado,conexion_activa,mensajeBoletoSellado,cp,registraPago,comienzaLectura,comienzaCambio,NoCajero,cajeroSuspendido,suspenderCajero,w,conteoPantallaPrincipal,inicioPago,imprime,cambiaColor,nom,loc,nivelDeCambio,cambio,leido,total,aux_cambio,aux_cambio1,pagado,config,monedas,monedasTotal,dineroTotal,avis,dineroTotalB,billetesTotales,billetes,tarifaVoluntaria,mensajeBoletoUsado,mensajeBoletoPerdido,mostrarTiempoDeSalidaRestante,mensajeError,mensajeAyuda
			#self.cambio.display(aux_cambio)
			#entrada0 = pulsos.X[0].obtenerValor()

			
			#print (a, b)
			self.lcobrar.setText("$"+str(aux_tarifa))
			self.ldepositar.setText("$"+str(total))
			#self.fol.setText(fo)
			#self.pen.setText(pe)
			self.he.setText(hh)
			self.hs.setText(hsalida)
			self.ttotal.setText(aux_dif)
			self.he2.setText(hh)
			self.hs2.setText(hsalida)
			self.ttotal2.setText(aux_dif)
			
			self.lrecarga1.setText(str(int(sensores.getValue('MONEDERO','limite_moneda_1')) - int(sensores.getValue('MONEDERO','moneda_1'))))
			self.lrecarga2.setText(str(int(sensores.getValue('MONEDERO','limite_moneda_2')) - int(sensores.getValue('MONEDERO','moneda_2'))))
			self.lrecarga5.setText(str(int(sensores.getValue('MONEDERO','limite_moneda_3')) - int(sensores.getValue('MONEDERO','moneda_3'))))
			self.lrecarga10.setText(str(int(sensores.getValue('MONEDERO','limite_moneda_4')) - int(sensores.getValue('MONEDERO','moneda_4'))))
			
			self.lfaltante1.setText(str(FALTANTE[0]))
			self.lfaltante2.setText(str(FALTANTE[1]))
			self.lfaltante3.setText(str(FALTANTE[2]))
			self.lfaltante4.setText(str(FALTANTE[3]))
			self.lfaltante5.setText(str(FALTANTE[4]))

			
			#self.nomPlaza.setText(nom)
			#self.nomLoc.setText(loc)
			#self.nomPlaza_2.setText(nom)
			#self.nomLoc_2.setText(loc)

			#self.aviso.setText(str(avis))
			if(secuencia_recarga == 1):
				aceptarMonedas2()
			
			elif(secuencia_recarga == 2):
				aceptarMonedas2()
				secuencia_recarga = 0

				

			if(cambiaColor==1):
				cambiaColor=0
				self.gdepositar.setStyleSheet("background-color: rgb(48, 48, 48,80%);")
				self.gfp.setStyleSheet("background-color: rgb(48, 48, 48,80%);border-radius:10%;")
				self.gp.setStyleSheet("background-color:rgb(101, 179, 0);border-radius:10%;")
				self.gav.setStyleSheet("background-color:rgb(101, 179, 0);border-radius:10%;")

			if(conexion_activa):
				#DESHABILITAR CAJERO LUEGO DE UN TIEMPO
				#inicioPago=1
				self.bwifi.setEnabled(True)
			else:
				self.bwifi.setEnabled(False)
				
				
			if(leido == 1):
				#DESHABILITAR CAJERO LUEGO DE UN TIEMPO
				#inicioPago=1
				self.secuenciaCobro(2)
				comienzaLectura=1
				leido = 0
				
			#if(entrada0 == 1 and aux_tarifa>0):
			#	cp = 1
				
			if(comienzaCambio==1):
				
				"""self.gcambio.setStyleSheet("background-color:rgb(17, 58, 8);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(27, 68, 18);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(37, 78, 28);")
				self.gcambio.setStyleSheet("background-color:rgb(47, 88, 38);")
				self.gcambio.setStyleSheet("background-color:rgb(57, 98, 48);")
				self.gcambio.setStyleSheet("background-color:rgb(67, 10, 58);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(67, 10, 58);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(77, 118, 68);")
				self.gcambio.setStyleSheet("background-color:rgb(87, 128, 78);")
				time.sleep(.2)
				self.gcambio.setStyleSheet("background-color:rgb(97, 138, 88);")
				self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				self.gdepositar.setStyleSheet("background-color:rgb(255, 255, 255);")
				self.lcobrar.setStyleSheet("background-color:rgb(255, 255, 255);")"""
				#pagado=1
				pass
			#if(cajeroSuspendido==1):
			#	self.stackedWidget.setCurrentIndex(14)
				
				
				
			if(pagado==1):
				pass
				#pagado=0
			
			if(pagado==2 or CobroFinalizado==1):
				pagado=0
				CobroFinalizado = 0
				print("Cajero Suspendido:",suspenderCajero)
				if(suspenderCajero==1):
					#self.stackedWidget.setCurrentIndex(14)
					#conteoPantallaPrincipal=1
					inicioPago=0
					w=0
				else:
					if(cp==1):
						self.stackedWidget.setCurrentIndex(13)
					else:
						self.stackedWidget.setCurrentIndex(2)
					conteoPantallaPrincipal=1
					inicioPago=0
					w=0
			if(config==1):
				config=2
				self.lmodelo.setVisible(False)
				self.lserie.setVisible(False)
				self.stackedWidget.setCurrentIndex(9)

			if(mostrarTiempoDeSalidaRestante[0]==1):
				self.avisoInserta.setText(mostrarTiempoDeSalidaRestante[1]+" MINUTOS PARA SALIR")

			if(mensajeBoletoSellado==1):
				self.avisoInserta.setText("DESCUENTO APLICADO")
			
			if(mensajeBoletoUsado==1):
				self.avisoInserta.setText("Este boleto ya fue usado")

			if(mensajeBoletoPerdido==1):
				self.avisoInserta.setText("Acude a atencion a clientes")

			if(mensajeError==1):
				self.avisoInserta.setText("Lo sentimos, intentelo de nuevo")

			if(mensajeAyuda==1):
				self.avisoInserta.setText("Tu peticion esta siendo procesada")
				self.bayudaCliente.setEnabled(False)
				self.bayudaCliente2.setEnabled(False)

			if(nivelDeCambio!=0):
				self.aviso2.setText("No cuento con mucho cambio")
				#self.gav.setStyleSheet("background-color: rgb(134, 0, 0);border-radius:10%;")
				
			if(nivelDeCambio==0):
				self.aviso2.setText("")
				#self.gav.setStyleSheet("background-color:rgb(101, 179, 0);border-radius:10%;")
			if(tarifaVoluntaria==1):
				os.system("wmctrl -a 'Dialog'")
				self.stackedWidget.setCurrentIndex(8)
				self.valvol.setText("$")
				tarifaVoluntaria=0

			QtCore.QTimer.singleShot(5,self.montos)

			if(self.chtodos.checkState()==2):
				self.chlunes.setCheckState(2)
				self.chmartes.setCheckState(2)
				self.chmiercoles.setCheckState(2)
				self.chjueves.setCheckState(2)
				self.chviernes.setCheckState(2)
				self.chsabado.setCheckState(2)
				self.chdomingo.setCheckState(2)

			if(self.ch1.checkState()==2):
				self.i1.setEnabled(True)
				self.i2.setEnabled(True)
			if(self.ch1.checkState()==0):
				self.i1.setEnabled(False)
				self.i2.setEnabled(False)
			if(self.ch2.checkState()==2):
				self.f1.setEnabled(True)
				self.f2.setEnabled(True)
			if(self.ch2.checkState()==0):
				self.f1.setEnabled(False)
				self.f2.setEnabled(False)
			if(self.ch3.checkState()==2):
				self.h1.setEnabled(True)
				self.h2.setEnabled(True)
			if(self.ch3.checkState()==0):
				self.h1.setEnabled(False)
				self.h2.setEnabled(False)
			if(self.ch4.checkState()==2):
				self.chtodos.setEnabled(True)
				self.chlunes.setEnabled(True)
				self.chmartes.setEnabled(True)
				self.chmiercoles.setEnabled(True)
				self.chjueves.setEnabled(True)
				self.chviernes.setEnabled(True)
				self.chsabado.setEnabled(True)
				self.chdomingo.setEnabled(True)
			if(self.ch4.checkState()==0):
				self.chtodos.setEnabled(False)
				self.chlunes.setEnabled(False)
				self.chmartes.setEnabled(False)
				self.chmiercoles.setEnabled(False)
				self.chjueves.setEnabled(False)
				self.chviernes.setEnabled(False)
				self.chsabado.setEnabled(False)
				self.chdomingo.setEnabled(False)
			#botones.manteniendoElCero()




		def boton_asistencia(self):
			pass

		def contadorSegundos(self):
			global cambio_faltante,tiempoBillExc,tl,tiempoLimBill,cp,varc,comienzaCambio,cajeroSuspendido,suspenderCajero,tarifasAplicadas,ma,preguntarPorEstado,accesoAcaja,c,conteoPantallaPrincipal,aux_cambio,cambio,total,w,killer,aux_tarifa,inicioPago,tiempoAgotadoDePago,cs2,cs1,v,a,p,q,y,z,mostrarTiempoDeSalidaRestante,mensajeBoletoPerdido,mensajeBoletoUsado,mensajeBoletoSellado,sel,mensajeError,mensajeAyuda
			#QtCore.QTimer.singleShot(1000,self.contadorSegundos)
			
			fehoy=str(datetime.now().date()).split('-',2)
			fehoy=fehoy[2]+"/"+fehoy[1]+"/"+fehoy[0]
			#self.ldate.setText(fehoy)
			self.ldate2.setText(fehoy)
			#self.ltime.setText(time.strftime("%H:%M:%S"))
			self.ltime2.setText(time.strftime("%H:%M:%S"))
			

			

			if(suspenderCajero == 1):
				self.secuenciaSuspension(1,cambio_faltante)
				suspenderCajero=0
				#cajeroSuspendido=1
				cambio_faltante = 0

				'''print("Se ha suspendido el cajero")
				self.secuenciaCobro(0)
				y=0
				#cajeroSuspendido=0
				conteoPantallaPrincipal=0
				aux_tarifa = 0
				aux_tarifa1 = 0
				total = 0
				cp=0
				tiempoBillExc=0
				self.lscan.setText('')
				registraPago=0
				aux_tarifa=0
				aux_cambio=0
				tarifasAplicadas=""
				self.aviso1.setText("")
				self.lcambio.setText("$0")
				os.system("wmctrl -a 'zbar'")
				#self.labelCambio.setText("$0")
				print("AQUI ANDAMOS")
				leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
				leerArch.write('')
				leerArch.close()
				killer=0
				'''



				print("Cobro finalizado, cajero suspendido")
				self.secuenciaCobro(0)
				y=0
				suspenderCajero = 0
				conteoPantallaPrincipal=0
				aux_tarifa = 0
				aux_tarifa1 = 0
				total = 0
				cp=0
				tiempoBillExc=0
				self.lscan.setText('')
				registraPago=0
				aux_tarifa=0
				aux_cambio=0
				tarifasAplicadas=""
				self.aviso1.setText("")
				self.lcambio.setText("$0")
				os.system("wmctrl -a 'zbar'")
				#self.labelCambio.setText("$0")
				print("AQUI ANDAMOS")
				leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
				leerArch.write('')
				leerArch.close()
				killer=0
				
					
					
			if(tiempoLimBill==1):
				tl=tl+1
				if(tl==10): #3 MINUTOS TOLERANCIA
					tl=0
					tiempoLimBill=0
					tiempoBillExc=1
					print("Tiempo EXcedido Billetero")
					
			if(preguntarPorEstado==0):
				cs1=cs1+1
				if(cs1==1): #3 MINUTOS TOLERANCIA
					cs1=0
					preguntarPorEstado=1
			if(mensajeError==1):
				v=v+1
				if(v==3): #3 MINUTOS TOLERANCIA
					v=0
					mensajeError=0
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(mensajeAyuda==1):
				ma=ma+1
				if(ma==3): #3 MINUTOS TOLERANCIA
					ma=0
					mensajeAyuda=0
					self.bayudaCliente.setEnabled(True)
					self.bayudaCliente2.setEnabled(True)
					#botones.prenderMonedero()
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(mensajeBoletoUsado==1):
				p=p+1
				if(p==3): #3 MINUTOS TOLERANCIA
					p=0
					mensajeBoletoUsado=0
					self.avisoInserta.setText("INSERTE EL TICKET")
					
			if(mensajeBoletoSellado==1):
				sel=sel+1
				if(sel==3): #3 MINUTOS TOLERANCIA
					sel=0
					mensajeBoletoSellado=0
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(mensajeBoletoPerdido==1):
				c=c+1
				if(c==3): #3 MINUTOS TOLERANCIA
					c=0
					mensajeBoletoPerdido=0
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(mostrarTiempoDeSalidaRestante[0]==1):
				q=q+1
				if(q==3): #3 MINUTOS TOLERANCIA
					q=0
					mostrarTiempoDeSalidaRestante[0]=0
					self.avisoInserta.setText("INSERTE EL TICKET")

			if(inicioPago==1):
				w=w+1
				if(w==300): #3 MINUTOS TOLERANCIA
					w=0
					tiempoAgotadoDePago=1
					inicioPago=0
					aux_tarifa = 0
					aux_tarifa1 = 0
					total = 0
					aux_tarifa=0
					aux_cambio=0
					registraPago=0
					tarifasAplicadas=""
					self.aviso1.setText("")
					self.secuenciaCobro(1)
					leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()
					killer=0


			if(conteoPantallaPrincipal == 1):
				y=y+1
				if(y==4):
					
					
					print("Cobro finalizado")
					self.secuenciaCobro(1)

						
					y=0
					suspenderCajero = 0
					conteoPantallaPrincipal=0
					aux_tarifa = 0
					aux_tarifa1 = 0
					total = 0
					cp=0
					tiempoBillExc=0
					self.lscan.setText('')
					registraPago=0
					aux_tarifa=0
					aux_cambio=0
					tarifasAplicadas=""
					self.aviso1.setText("")
					self.lcambio.setText("$0")
					os.system("wmctrl -a 'zbar'")
					#self.labelCambio.setText("$0")
					print("AQUI ANDAMOS")
					leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()
					killer=0
					

			if(accesoAcaja==1):
				z=z+1
				if(z==60):
					z=0
					accesoAcaja=0
					botones.cerrarPuerta()

			QtCore.QTimer.singleShot(1000,self.contadorSegundos)
			
		def contadorMiliSegundos(self):
			global varl,comienzaCobro,comienzaCambio,varc,red,green,blue,leido,comienzaLectura,rrr
			"""
			if(comienzaLectura==1):
				self.aviso1.setText("")
				varl=varl+1
				if(red<59):
					rrr=1
				if(red>150):
					rrr=0
				if(rrr==0):
					red=red-10
					green=green-10
					blue=blue-10
				else:
					red=red+5
					green=green+5
					blue=blue+5
				self.gcambio.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.lcambio.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				#self.gcobrar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.lcobrar.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#self.lcobrar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#print("red",red,green,blue)
				#self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				if(varl==30):
					varl=0
			"""

			if(comienzaLectura==1):
				self.aviso1.setText("")
				varl=varl+1
				if(red<59):
					rrr=1
				if(red>105):
					rrr=0
				if(rrr==0):
					red=red-5
					green=green-5
					blue=blue-5
				else:
					red=red+5
					green=green+5
					blue=blue+5
				self.gcambio.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.lcambio.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				#self.gcobrar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.lcobrar.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#self.lcobrar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#print("red",red,green,blue)
				#self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				if(varl==30):
					varl=0
			
					
			if(comienzaCobro==1):
				self.aviso1.setText("")
				comienzaLectura=0
				varl=varl+1
				if(red<59):
					rrr=1
				if(red>105):
					rrr=0
				if(rrr==0):
					red=red-5
					green=green-5
					blue=blue-5
				else:
					red=red+5
					green=green+5
					blue=blue+5
				"""self.gcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.lcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.gdepositar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.ldepositar.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				"""
				self.gcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.lcobrar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.ldepositar.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#print("red",red,green,blue)
				#self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				if(varl==30):
					varl=0
					
			
					
					
			
			if(comienzaCambio==1):
				self.secuenciaCobro(3)
				comienzaCambio=0
				comienzaLectura=0
				comienzaCobro=0
				self.aviso1.setText("Espere su cambio... "+str(aux_cambio))
				#self.labelCambio.setText("$"+str(aux_cambio))
				self.lcambio.setText("$"+str(aux_cambio))
				varc=varc+1
				if(red<59):
					rrr=1
				if(red>105):
					rrr=0
				if(rrr==0):
					red=red-5
					green=green-5
					blue=blue-5
				else:
					red=red+5
					green=green+5
					blue=blue+5
				"""self.gdepositar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.ldepositar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.gcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.lcobrar.setStyleSheet("background-color:rgb(220, 220, 220);")
				self.gcambio.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.lcambio.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")"""
				self.gdepositar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.ldepositar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.gcobrar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.lcobrar.setStyleSheet("background-color:rgb(220, 220, 220);color:rgb(105,105,105);")
				self.lcambio.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.aviso1.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.avisoInserta_2.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				
				#print("red",red)
				#self.gcambio.setStyleSheet("background-color:rgb(107, 148, 98);")
				if(varc==10):
					varc=0
					#pagado=1
					#red=17
					#green=58
					#blue=8
			if(aux_tarifa==0):
				comienzaCambio=0
				varl=varl+1
				if(red<50):
					rrr=1
				if(red>150):
					rrr=0
				if(rrr==0):
					red=red-10
					green=green-10
					blue=blue-10
				else:
					red=red+10
					green=green+10
					blue=blue+10
				
				#self.gbol.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				#self.avisoInserta.setStyleSheet("background-color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");")
				self.avisoInserta.setStyleSheet("color:rgb("+str(red)+", "+str(green)+", "+str(blue)+");background-color:transparent;")
				#print("red",red)
			QtCore.QTimer.singleShot(.3,self.contadorMiliSegundos)
			


		def actualiza(self,val):
			print(val)

		def cambia(self,num):
			self.stackedWidget.setCurrentIndex(num)



	app = QApplication(sys.argv)
	_ventana = Ventana()
	_ventana.show()
	app.exec_()



def restar_hora(horab,fechab):
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
		aux_dif=(str(restaFechas).split('.',1))[0]
		dias = int(restaFechas.days)
		horas = int(restaFechas.seconds / 3600)
		print("****RES:",restaFechas)
		return dias,horas



def calculaTarifa(tiempoEstacionado,descuento):
	global costillo,tarifa,aux_tarifa,aux_tarifa1,aux_dif,tarifaVoluntaria,tarifaSeleccionada
	aplicaDescuento=0
	indicador=0
	costillo=0
	horasRestantes=0
	dicdias = {'LUNES':'lunes','MARTES':'martes','MIERCOLES':'miercoles','JUEVES':'jueves','VIERNES':'viernes','SABADO':'sabado','DOMINGO':'domingo'}
	#dicdias = {'MONDAY':'lunes','TUESDAY':'martes','WEDNESDAY':'miercoles','THURSDAY':'jueves','FRIDAY':'viernes','SATURDAY':'sabado','SUNDAY':'domingo'}
	fechaActual = datetime.now().date()
	tiempoActual = datetime.now().time()
	#print("222",ahora,ahora2)
	t=time.localtime()
	dias=time.strftime("%A",t)
	#diaDeLaSemana=dicdias[dias.upper()]
	diaDeLaSemana="lunes"
	print("cuatro datos:)----->",fechaActual,tiempoActual,tiempoEstacionado,diaDeLaSemana)
	print("El descuento ES:::::::::",descuento,type(descuento))
	try:
		if(descuento==1):
			print("-.-.-.NO DESCUENTO",descuento)
			#cur.execute("select * from \"TARIFA\" where estado=1 order by costo Asc")
			cur.execute("select * from \"TARIFA\" where estado=1 and descuento=%s order by prioridad Desc",(str(descuento)))
		else:
			print("-.-.-.SI DESCUENTO",descuento)
			cur.execute("select * from \"TARIFA\" where estado=1 and descuento=%s order by prioridad Desc",(str(descuento)))
			#aplicaDescuento=1


		for reg in cur:
			print(reg[0],reg[1],reg[2],reg[3],reg[4],reg[5],reg[6],reg[7],reg[8],reg[9],reg[10],reg[11])
			if(str(reg[2])!="None"):
				if(fechaActual>=reg[2] and fechaActual<=reg[3]):
					print("FECHA ENTRA")
				else:
					indicador=indicador+1
			if(str(reg[4])!="None"):
				if(tiempoActual>=reg[4] and tiempoActual<=reg[5]):
					print("HORA ENTRA")
				else:
					indicador=indicador+1

			if(str(reg[6])!="None"):
				if(diaDeLaSemana in str(reg[6])):
					print("Dia de la semana entra")
				else:
					indicador=indicador+1

			if(str(reg[9])!="None"):
				if(tiempoEstacionado>=int(reg[9]) and tiempoEstacionado<int(reg[10])):
					print("INTERVALO ENTRA")
				else:
					indicador=indicador+1

			print("!!!!!",indicador)
			if(aplicaDescuento==1):
				indicador=0
			if(indicador==0):
				aplicaDescuento=0
				cantidadDeHor=reg[10]
				horasRestantes=tiempoEstacionado-cantidadDeHor
				tarifaSeleccionada=reg[0]
				costillo=reg[8]
				break
			else:
				indicador=0



		print("costillo=",costillo)
		if(costillo!=0):
			aux_tarifa=aux_tarifa+costillo
		else:
			print("NO SE APLICO NINGUNA TARIFA")
			#aux_tarifa=0
			tarifaVoluntaria=1
		print(aux_tarifa)
		print("respuesta: ")
		return tarifaSeleccionada,horasRestantes
	except:
		tarifaVoluntaria=1
		print('Error al accesar a la base de datos')
		return 13,0	


def buscaCamara():
	global camInicial
	while(1):
		lee2 = os.system("sudo find /dev -name 'video*' > cam.txt")
		a = open("cam.txt", "r")
		cam=(a.readline().rstrip("\n")).lstrip("\x00")
		a.close()
		a = open("cam.txt", "w")
		a.write('')
		#time.sleep(1)
		#print('Cammmmmmmmm',cam,camInicial)
		if(cam!=camInicial):
			#print('Camara desconectadaaaaaaaaa')
			os.system("sudo pkill zbarcam")

def leerArchivo():
	global Boleto,conexion_activa,aportacionConfirmada,tarifaVoluntaria,cajeroSuspendido,preguntarPorEstado,leido,fo,pe,fe,hh,hsalida,kill,killer,killbill,config,fechaAMD,nivelDeCambio,h,nivelActual,aux_tarifa,imprime,NoCajero,tarifaSeleccionada,mostrarTiempoDeSalidaRestante,mensajeBoletoPerdido,mensajeBoletoUsado,mensajeBoletoSellado,tarifasAplicadas,mensajeError
	tarifaSeleccionada=0
	A=0
	estadoConexion = 0
	#mixer.init()
	#mixer.music.load('/home/pi/Downloads/beep-08b.wav')
	while(kill == 0):
		#if(imprime==1):
		if(imprime==5):
			#imp()
			fe=fe+" "+hh
			fec=datetime.now().date()
			fec=str(fec.day)+"/"+str(fec.month)+"/"+str(fec.year)+','+hh+','+str(aux_tarifa)+','+fo+','+pe
			leerArch = open(rutaUsuario+"Documentos/pago.txt", "a+")
			leerArch.write(fec)
			leerArch.close()
			os.system("sudo python3 /home/cajero/Documentos/cajero/archimp.py")
			
			

			imprime=0


		while(killer == 0 and kill == 0):
			#leerArch = open(rutaUsuario+"Documentos/ticket.txt", "r")
			#folio=leerArch.readline().rstrip("\n")
			#time.sleep(.2)
			if len(Boleto) > 0:
				print("Boleto,",Boleto)
			#if(folio != ''):
				#print("{}  ==  {}".format(folio,"Estacionamientos unicos de Mexico"))
				#booleana=str("Estacionamientos unicos de Mexico") in str(folio)
				if(str("M") in str(Boleto[0])):
					#os.system('sudo python3 /home/pi/scanner/buz.py')
					#mixer.music.play()
					#time.sleep(1)
					#pass
					#print(folio)
					if(str(Boleto[0]) == 'boleto perdido'):
						leerArch.close()
						leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
						leerArch.write('')
						leerArch.close()

						cur.execute("select * from \"TARIFA\" where des_tar='boleto perdido' order by prioridad Desc")
						for reg in cur:
							print(reg[0],reg[1],reg[2],reg[3],reg[4],reg[5],reg[6],reg[7],reg[8],reg[9],reg[10],reg[11])
							if(str(reg[7])=="boleto perdido"):
								aux_tarifa=reg[8]
								leido = 1
								killbill = 0
								habilitarDispositivosCobro(estadoConexion)
					else:

						#impresora.imprimirBoletoC2("12/12/17","02:00:00",9)
						killer = 1
						#leerArch.close()
						
						
						#leerArch = open(rutaUsuario+"Documentos/ticket.txt", "r")
						
						'''
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
						hsalida=hora.mostrarHoraSinFormato()[0]+":"+hora.mostrarHoraSinFormato()[1]+":"+hora.mostrarHoraSinFormato()[2]
						h=readQR[3].rstrip("\n")
						fe = readQR[2].rstrip("\n")
						'''
						hsalida=hora.mostrarHoraSinFormato()[0]+":"+hora.mostrarHoraSinFormato()[1]+":"+hora.mostrarHoraSinFormato()[2]
						fo = Boleto[1]
						pe = Boleto[2]
						hh = Boleto[4]
						h = Boleto[4]
						fe = Boleto[3]
						print("Boleto: ",Boleto)
						Boleto = ""
						#leerArch.close()
						#leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
						#leerArch.write('')
						#leerArch.close()
						print("FEEEE>>>>>",fo)
						#Verificar nivel de cambio
						
						if(str("Admin") in str(fo)):
						#if(int(fo)==1566):

							print("Modo admin ON")
							config=1
							while(config!=0):
								if(preguntarPorEstado==1):
									monitorearChanger()
									preguntarPorEstado=0
								time.sleep(.5)
								killer=0
							print("Modo admin OFF")
							break
						else:
							#if(cajeroSuspendido==1):
							#	A=-1
								#self.cambia(13)
							#	pass
							if 1:
								h1=str(hora.mostrarHoraSinFormato()[0])+":"+str(hora.mostrarHoraSinFormato()[1])+":"+str(hora.mostrarHoraSinFormato()[2])
								#Se obtiene la cantidad de horas y minutos que el cliente estuvo en el estacionamiento
								horaBoleto=h.split(':',2)
								fechaAMD=fe.split('-',2)
								print("fechas----->",fe,fechaAMD)
								fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]
								mensaje = str(fo) + "," + str(pe) + "," + fechaAMD +" "+h
								print(mensaje,type(mensaje))
								#return 2
								resultado=Servidor.configSocket("informacion boleto", mensaje)
								print("resultado",resultado)
								if(not conexion_activa or resultado == -1):
									estadoConexion = 0
									#print("ERROR EN LA COMUNICACION")
									#A=-1
									#mensajeError=1
									
									
									leerArch = open(ruta+"../../sys/descuento.txt", "r")
									sello=leerArch.readline().rstrip("\n")
									print("sellado =",sello)
									if(int(sello) == 1):
										descuento=2
									else:
										descuento=1
									leerArch.close()
									leerArch = open(ruta+"../../sys/descuento.txt", "w")
									leerArch.write('0')
									leerArch.close()
									#Verificando sello de boleto Fin
									estadoBoleto=1
									
									
									
									#fechaBoleto=resultado[2]
									print(fechaAMD,horaBoleto)
									dh=restar_hora(horaBoleto,fechaAMD.split('-'))
									#ESTE IF ES PARA APLICAR TARIFA MAXIMA
									dias=dh[0]
									horas=dh[1]
									tiempoEstacionado=horas
									if(dias!=0):
										tiempoEstacionado=15
									if(descuento==2):
										A=0
										respuesta=calculaTarifa(tiempoEstacionado,2)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
									elif(int(estadoBoleto)==1):
										A=0
										print("<<<<>>>> DIAS, TE , Estado B,descuento :",dias,tiempoEstacionado,estadoBoleto,descuento)
										#BOLETO NO PAGADO, SI PAGADO=AUN TIENES TIEMPO X PARA SALIR, TIEMPO EXCEDIDO, BOLETO USADO
										respuesta=calculaTarifa(tiempoEstacionado,descuento)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
										print(tarifasAplicadas)
										if(respuesta[1]<0):
											print("respuesta de tarifa =",respuesta)
										else:
											segundaRespuesta=calculaTarifa(respuesta[1],1)
											tarifasAplicadas=tarifasAplicadas+";"+str(segundaRespuesta[0])
									elif(int(estadoBoleto)==2):
										A=-1
										mostrarTiempoDeSalidaRestante[0]=1
										mostrarTiempoDeSalidaRestante[1]=str(resultado[2])
									elif(int(estadoBoleto)==3):
										A=0
										fechaBoleto=fechaBoleto.split(" ",1)
										fechaAMD=fechaBoleto[0].split('-',2)
										fechaAMD=fechaAMD[0]+"-"+fechaAMD[1]+"-"+fechaAMD[2]
										#fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]
										print(fechaBoleto[1].split(':',2),fechaAMD)
										dh2=restar_hora(fechaBoleto[1].split(':',2),fechaAMD.split('-'))
										dias=dh2[0]
										horas=dh2[1]
										if(dias!=0):
											tiempoEstacionado=23
										tiempoEstacionado=horas
										r=calculaTarifa(tiempoEstacionado,1)
										tarifasAplicadas=str(r[0])
									elif(int(estadoBoleto)==4):
										A=-1
										mensajeBoletoUsado=1
									elif(int(estadoBoleto)==5):
										A=0
										respuesta=calculaTarifa(tiempoEstacionado,1)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
								
								#elif(resultado[0]==''):
								#	A=-1
								#	mensajeBoletoUsado=1
								else:
									estadoConexion = 1
									boleterasConectadas = 1
									
									
									"""
									Aqui se verifica el estado de conexion de las boleteras , en caso de estar conectadas y no existir el boleto,
									no se iniciara el proceso de pago,
									
									
									en caso contrario puede que exista el boleto y aun no ha sido registrado, por lo tanto se iniciara el pago 
									pasando como argumento el estado de la conexion.
									
									estadoConexionBoleteras = conexion.obtenerEstadoBoleteras()
									
									"""
									if(boleterasConectadas): 
										#resultado=Servidor.configSocket("informacion boleto", mensaje)
										#print("resultado",resultado)
										pass
									else:
										resultado = [1,fechaAMD]
									#Verificando sello de boleto
									leerArch = open(ruta+"../../sys/descuento.txt", "r")
									sello=leerArch.readline().rstrip("\n")
									print("sellado =",sello)
									if(int(sello) == 1):
										descuento=2
									else:
										descuento=1
									leerArch.close()
									leerArch = open(ruta+"../../sys/descuento.txt", "w")
									leerArch.write('0')
									leerArch.close()
									#Verificando sello de boleto Fin
									estadoBoleto=int(resultado[1])#ESTADO=2,FECHA=MINUTOS RESTANTES PARA SALIR....E=4,F=NULL,D=0....E=1,COBRAR NORMAL....
									
									fechaBoleto=resultado[2]
									print(fechaAMD,horaBoleto)
									dh=restar_hora(horaBoleto,fechaAMD.split('-'))
									#ESTE IF ES PARA APLICAR TARIFA MAXIMA
									dias=dh[0]
									horas=dh[1]
									tiempoEstacionado=horas
									if(dias!=0):
										tiempoEstacionado=15
									if(descuento==2):
										A=0
										respuesta=calculaTarifa(tiempoEstacionado,2)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
									elif(int(estadoBoleto)==1):
										A=0
										print("<<<<>>>> DIAS, TE , Estado B,descuento :",dias,tiempoEstacionado,estadoBoleto,descuento)
										#BOLETO NO PAGADO, SI PAGADO=AUN TIENES TIEMPO X PARA SALIR, TIEMPO EXCEDIDO, BOLETO USADO
										respuesta=calculaTarifa(tiempoEstacionado,descuento)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
										print(tarifasAplicadas)
										if(respuesta[1]<0):
											print("respuesta de tarifa =",respuesta)
										else:
											segundaRespuesta=calculaTarifa(respuesta[1],1)
											tarifasAplicadas=tarifasAplicadas+";"+str(segundaRespuesta[0])
									elif(int(estadoBoleto)==2):
										A=-1
										mostrarTiempoDeSalidaRestante[0]=1
										mostrarTiempoDeSalidaRestante[1]=str(resultado[2])
									elif(int(estadoBoleto)==3):
										A=0
										fechaBoleto=fechaBoleto.split(" ",1)
										fechaAMD=fechaBoleto[0].split('-',2)
										fechaAMD=fechaAMD[0]+"-"+fechaAMD[1]+"-"+fechaAMD[2]
										#fechaAMD=fechaAMD[2]+"-"+fechaAMD[1]+"-"+fechaAMD[0]
										print(fechaBoleto[1].split(':',2),fechaAMD)
										dh2=restar_hora(fechaBoleto[1].split(':',2),fechaAMD.split('-'))
										dias=dh2[0]
										horas=dh2[1]
										if(dias!=0):
											tiempoEstacionado=23
										tiempoEstacionado=horas
										r=calculaTarifa(tiempoEstacionado,1)
										tarifasAplicadas=str(r[0])
									elif(int(estadoBoleto)==4):
										A=-1
										mensajeBoletoUsado=1
									elif(int(estadoBoleto)==5):
										A=0
										respuesta=calculaTarifa(tiempoEstacionado,1)
										tarifasAplicadas=tarifasAplicadas+str(respuesta[0])
								#A=calculaTarifa(tiempoEstacionado)

								#A=calculaTarifa("10:01:00")
						if(A!=-1):
							print("Iniciando cobro....",aux_tarifa,tarifasAplicadas)
							#REGISTRA BOLETO EN BD C/CONEXION
							tarifasAplicadas = 13
							tarifaSeleccionada = 13
							#consu="insert into \"BOLETO\"(tarifa,cajero,tipo,estado,conexion,estado_final,folio,expedidora,\"fechaExpedicion\") values("+str(tarifaSeleccionada)+","+str(NoCajero)+",1,"+str(estadoBoleto)+","+str(estadoConexion)+","+str(0)+","+str(fo)+",'"+str(pe)+"','"+fe+" "+h+"')"
							#cur.execute(consu)
							#conn.commit()
							while(aux_tarifa==0):
								time.sleep(.5)
								if(aportacionConfirmada==1):
									aportacionConfirmada=0
									
									break
							
							if(aux_tarifa==0):
								count(ser,estadoConexion)
							else:
								leido = 1
								os.system("wmctrl -a 'Dialog'")
								#enable_coin(ser)
								#enable_sequence(ser)
								killbill = 0
								habilitarDispositivosCobro(estadoConexion)
								
							
						else:
							killer=0

				elif(str("L") in str(Boleto[0])):
					#Si existe el descuento entonces 1
					Boleto = ""
					descuento = 1
					leerArch = open(ruta+"../../sys/descuento.txt", "w")
					if (descuento):
						mensajeBoletoSellado = 1
						leerArch.write('1')
						leerArch.close()
					else:
						leerArch.write('0')
						leerArch.close()
					leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()

				else:
					leerArch.close()
					leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
					leerArch.write('')
					leerArch.close()
			else:
				#leerArch.close()
				pass
				#time.sleep(.5)




def aceptarBilletes(estadoConexion,TON):
	global cp,cambio,tarifa,aux_cambio,aux,rep,ser,aux_tarifa,total,bill,killbill,ESTADO_BILLETERO
	#print("Otra y otra")
	TON.actualizar()
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51 , 1 , 51 , 0])
	ser.write(a);
	time.sleep(.01)
	rBill = ser.read(6)
	#rBill = '\t'
	print("bi",rBill)
	if(rBill):
		if(rBill[0]==144 or rBill[0]==145 or rBill[0]==146 or rBill[0]==147 or rBill[0]==148):
			billeteConfirmado=1
			ESTADO_BILLETERO = 1
			#cambiaColor=1
			#disable_coin(ser)
			cambio = 0
			if(rBill[0]==144):
				bill = 20
				billetes[0]=billetes[0]+1
				billetesPago[0]=billetesPago[0]+1
			if(rBill[0]==145):
				bill = 50
				billetes[1]=billetes[1]+1
				billetesPago[1]=billetesPago[1]+1
			if(rBill[0]==146):
				bill = 100
				billetes[2]=billetes[2]+1
				billetesPago[2]=billetesPago[2]+1
			if(rBill[0]==147):
				bill = 200
				billetes[3]=billetes[3]+1
				billetesPago[3]=billetesPago[3]+1
			if(rBill[0]==148):
				bill = 500

			total = total+ bill
			#dineroTotalB=dineroTotalB+bill

			print(total)
			#time.sleep(.005)
			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
			ser.write(a);
			cambio = total - aux_tarifa
			accept_sequence(ser)
			count(ser,estadoConexion)
			#if(aux_cambio<0):
			#	enable_coin(ser)
			#	enable_coin(ser)
			#	enable_coin(ser)
				#enable_sequence(ser)

		elif rBill[0] == 0:
			ESTADO_BILLETERO = 1
			TON.entrada = 0
			TON.actualizar()
			
		else:
			if iniciarTemporizador(TON):
				ESTADO_BILLETERO = 0
				#break
				
	else:
		if iniciarTemporizador(TON):
			ESTADO_BILLETERO = 0
			#break
		
		


def aceptarBilletes2(estadoConexion,TON):
	global cp,cambio,tarifa,aux_cambio,aux,rep,ser,aux_tarifa,total,bill,killbill
	print("Otra y otra")
	TON = Temporizador("aceptarBilletes", 5)
	#while(1):
	#print("killbill",killbill)
	while(killbill == 0):
		#count(ser)
		#time.sleep(.050)
		time.sleep(.05)
		if(cp==1):
			count(ser)
		else:	
			if(killbill==1):
				pass
			else:
				#print("bill")
				time.sleep(.002)
				time.sleep(.002)

				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51 , 0 , 51 , 1])
				ser.write(a);

				time.sleep(.05)
				rBill = ser.read(6)
				print("bi",rBill)
				if(rBill):
					if(rBill[0]==144 or rBill[0]==145 or rBill[0]==146 or rBill[0]==147 or rBill[0]==148):
						billeteConfirmado=1
						#cambiaColor=1
						#disable_coin(ser)
						cambio = 0
						if(rBill[0]==144):
							bill = 20
							billetes[0]=billetes[0]+1
							billetesPago[0]=billetesPago[0]+1
						if(rBill[0]==145):
							bill = 50
							billetes[1]=billetes[1]+1
							billetesPago[1]=billetesPago[1]+1
						if(rBill[0]==146):
							bill = 100
							billetes[2]=billetes[2]+1
							billetesPago[2]=billetesPago[2]+1
						if(rBill[0]==147):
							bill = 200
							billetes[3]=billetes[3]+1
							billetesPago[3]=billetesPago[3]+1
						if(rBill[0]==148):
							bill = 500

						total = total+ bill
						#dineroTotalB=dineroTotalB+bill

						print(total)
						#time.sleep(.005)
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
						ser.write(a);
						cambio = total - aux_tarifa
						accept_sequence(ser)
						count(ser,estadoConexion)
						#if(aux_cambio<0):
						#	enable_coin(ser)
						#	enable_coin(ser)
						#	enable_coin(ser)
							#enable_sequence(ser)
					else:
						if iniciarTemporizador(TON):
							break
							
				else:
					if iniciarTemporizador(TON):
						break

def aceptarMonedas2():
	global secuencia_recarga
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
	ser.write(a);
	time.sleep(.05)
	r = ser.read(6)
	print("mo",r)
	if(r):
		print("A")
		if(r.__sizeof__() > 18):
			print("B")
			if (r[0] == 11):
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
				ser.write(a);
			elif(r[0] != 0 and r[0] !=11 and r[0]!=2 and r.__sizeof__() > 18):
				print("C")
				print(r)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
				ser.write(a);
				if (rep == 0):
					print("D")
					palPoll(ser,r[0], r)
					rep = 0
					#rep=1
			if (r[0] == 0):
				rep = 0

			
def aceptarMonedas(estadoConexion):
	global cp,cambio,tarifa,aux_cambio,aux,rep,ser,aux_tarifa,killbill
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
	ser.write(a);
	time.sleep(.05)
	r = ser.read(6)
	print("mo",r)
	if(r):
		print("A")
		if(r.__sizeof__() > 18):
			print("B")
			if (r[0] == 11):
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
				ser.write(a);
			elif(r[0] != 0 and r[0] !=11 and r[0]!=2 and r.__sizeof__() > 18):
				print("C")
				print(r)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0 , 0])
				ser.write(a);
				if (rep == 0):
					print("D")
					palPoll(ser,r[0], r)

					cambio = total - aux_tarifa
					aux_cambio=cambio
					count(ser,estadoConexion)

					rep = 0
					#rep=1
			if (r[0] == 0):
				rep = 0
	
			
def deshabilitarDispositivosCobro():
	self.disable_coin()
	self.disable_sequence()
def habilitarPolleo(estadoConexion):
	global secuencia_recarga
	resultadoConfiguracionMonedero = enable_coin(ser)

def habilitarDispositivosCobro(estadoConexion):
	global guardar,tipo_controladora,ESTADO_BILLETERO,tarifaVoluntaria,cp,tiempoAgotadoDePago,cambiaColor,total,bill,cambio,tarifa,aux_cambio,aux,rep,estatus,ser,killbill,aux_tarifa,bill,pagado,billetesTotales,dineroTotal,billetes,dineroTotalB,billetesPago
	
	resultadoConfiguracionMonedero = enable_coin(ser)
	resultadoConfiguracionBilletero = enable_sequence(ser)
	
	print("Habilitando aceptacion de dispositivos M/B",resultadoConfiguracionMonedero,resultadoConfiguracionBilletero)
	TON_01 = Temporizador("Aceptar Monedas", 5)
	TON_02 = Temporizador("Aceptar Billetes", 5)
	guardar.print("iniciando cobro...")
	
	


	while(killbill == 0):
		print("Estado Billetero:",ESTADO_BILLETERO)
		time.sleep(.01)
		ser.limpiar()
		


		if tipo_controladora == 0:
			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
			ser.write(a);
			time.sleep(.01)	

			
			r = ser.read(6)
			if (r):
				print ("BOTON", r, r[0], ord(Comunicacion.caracterDeInicio))

				if len(r) == 6:
					if r[0] == ord(Comunicacion.caracterDeInicio):
						if r[5] == ord(Comunicacion.caracterDeFin):
							print ("Boton", r[1])

							cp = (r[1]) & 1

		else:
			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.BOTON_CANCELAR)
			ser.write(a);
			time.sleep(.01)	

			
			r = ser.read(3)
			if (r):
				#print ("BOTON", r, r[0], ord(Comunicacion.caracterDeInicio))

				if len(r) == 3:
					if r[0] == ord(Comunicacion.caracterDeInicio):
						if r[2] == ord(Comunicacion.caracterDeFin):
							#print ("Boton", r[1])

							cp = (r[1] - ord('0')) & 1

		


		'''
		#############################Solicitando la temperatura ###################################
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.TEMPERATURA)
		ser.write(a);	
		time.sleep(.01)	
		r = ser.read(29)

		if (r):
			
			if comunicacion.verificarTrama(r):
				comunicacion.obtenerInstruccion(r)

			#if len(r) == 21:
			#	temp = unpack ('f', r[15: 15 + 4])[0]
			#	print ("temp ", temp)


		###########################################################################################
		'''

		
		


		if(cp==1):
			print("calculando montos...")
			count(ser, estadoConexion)
		else:
			if(resultadoConfiguracionMonedero == b'\x00'):
				aceptarMonedas(estadoConexion)
			
			if(killbill==1):
				pass
			else:
				if(resultadoConfiguracionBilletero == b'\x00' and ESTADO_BILLETERO):
					#print("aceptacion de billetes...")
					aceptarBilletes(estadoConexion,TON_02)

		



def billf():
	global tarifaVoluntaria,cp,tiempoAgotadoDePago,cambiaColor,total,bill,cambio,tarifa,aux_cambio,aux,rep,estatus,ser,killbill,aux_tarifa,bill,pagado,billetesTotales,dineroTotal,billetes,dineroTotalB,billetesPago
	contadorErrorBilletero=0
	contadorErrorMonedero=0
	print("Otra y otra")
	while(killbill == 0):
		#count(ser)

		#time.sleep(.050)

		


		if(cp==1):
			#count(ser)
			calcularCambio(ser)
		
		else:	
			"""
			ser.parity = change_parity(0x0B, 1)
			ser.write(b'\x0B')
			ser.parity = change_parity(0x0B, 0)
			ser.write(b'\x0B')
			"""
			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
			ser.write(a);
			


			#time.sleep(.05) Tiempo Pred CajeroRed
			time.sleep(.05)
			#time.sleep(.002)
			r = ser.read(6)
			print("mo",r)
			
			if(r):
				print("A")
				if(r.__sizeof__() > 18):
					print("B")
					if (r[0] == 11):
						"""
						ser.parity = change_parity(0x00, 0)
						ser.write(b'\x00')
						"""
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);

					elif(r[0] != 0 and r[0] !=11 and r[0]!=2 and r.__sizeof__() > 18):
						print("C")
						print(r)
						"""
						ser.parity = change_parity(0x00, 0)
						ser.write(b'\x00')
						"""
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);

						if (rep == 0):
							print("D")
							palPoll(ser,r[0], r)

							cambio = total - aux_tarifa
							aux_cambio=cambio
							#count(ser)
							calcularCambio(ser)
							rep = 0
							#rep=1
					if (r[0] == 0):
						rep = 0
			else:
				contadorErrorMonedero = contadorErrorMonedero + 1
				print("No se recibieron datos en monedero: ",contadorErrorMonedero)

			if(killbill==1):
				pass
			else:
			
				print("c")
				time.sleep(.002)
				time.sleep(.002)
				"""
				ser.parity = change_parity(0x33, 1)
				ser.write(b'\x33')
				ser.parity = change_parity(0x33, 0)
				ser.write(b'\x33')
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51, 1, 51, 0])
				ser.write(a);


				time.sleep(.05)
				rBill = ser.read(6)
				print("bi",rBill)
				if(rBill):
					if(rBill[0]==144 or rBill[0]==145 or rBill[0]==146 or rBill[0]==147 or rBill[0]==148):
						billeteConfirmado=1
						#cambiaColor=1
						#disable_coin(ser)
						cambio = 0
						if(rBill[0]==144):
							bill = 20
							billetes[0]=billetes[0]+1
							billetesPago[0]=billetesPago[0]+1
						if(rBill[0]==145):
							bill = 50
							billetes[1]=billetes[1]+1
							billetesPago[1]=billetesPago[1]+1
						if(rBill[0]==146):
							bill = 100
							billetes[2]=billetes[2]+1
							billetesPago[2]=billetesPago[2]+1
						if(rBill[0]==147):
							bill = 200
							billetes[3]=billetes[3]+1
							billetesPago[3]=billetesPago[3]+1
						if(rBill[0]==148):
							bill = 500

						total = total+ bill
						dineroTotalB=dineroTotalB+bill

						print(total)
						#time.sleep(.005)
						"""
						ser.parity = change_parity(0x00, 0)
						ser.write(b'\x00')
						"""
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);
						time.sleep(.01)


						cambio = total - aux_tarifa
						accept_sequence(ser)
						#count(ser)
						calcularCambio(ser)
						if(aux_cambio<0):
							enable_coin(ser)
							#enable_coin(ser)
							#enable_coin(ser)
							#enable_sequence(ser)
				else: 
					contadorErrorBilletero = contadorErrorBilletero + 1
					print("No se recibieron datos en billetero: ",contadorErrorBilletero)

def monitorearChanger():
	global cartuchoRemovido
	ba = [0x0F, 0x05]
	ckInt = checkSum(ba)

	"""
	ser.parity = change_parity(0x0F, 1)
	ser.write(b'\x0F')
	ser.parity = change_parity(0x05, 0)
	ser.write(b'\x05')
	ser.parity = change_parity(int(ckInt), 0)
	ser.write(bytes([int(ckInt)]))
	"""

	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 5, 0])
	ser.write(a);
	time.sleep(.01)


	time.sleep(.005)
	r = ser.read(8)
	print("rut->",r)
	if(r):
		if(r[0]==21 and r[1]==2):
			cartuchoRemovido=1


def actualizaTubos():
	global cartuchoRemovido


def enable_sequence(ser):
	global ESTADO_BILLETERO
	#STAKER
	print("Configurando billetero")
	TON_01 = Temporizador("enable_sequence", 5)
	TON_02 = Temporizador("enable_sequence 2", 5)
	while(1):
		
		ser.limpiar()
		#ser.flushInput()
		
		'''
		time.sleep(.09)
		ser.parity = change_parity(0x36, 1)ser.parity = change_parity(0x36, 1)
		ser.write(b'\x36')
		ser.parity = change_parity(0x36, 0)
		ser.write(b'\x36')
		time.sleep(.09)
		
		'''

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [54, 1, 54, 0])
		ser.write(a);
		time.sleep(.01)
		ask = ser.read(1)
		#ask = b'\x03'
		
		
		
		print("eseq:",ask)
		if (ask):
			if(ask[0]==254):
				print("Pila llena")
				ESTADO_BILLETERO = 1
			elif(ask[0]==00):
				print("Pila Vacia")
				time.sleep(.2)
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				ESTADO_BILLETERO = 1
				#return ask
				break
			else:
				if iniciarTemporizador(TON_01):
					ESTADO_BILLETERO = 0
					break
		else:
			if iniciarTemporizador(TON_01):
				ESTADO_BILLETERO = 0
				break




	
	
	while(ESTADO_BILLETERO):
		"""
		time.sleep(.09)
		ser.parity = change_parity(0x34, 1)
		ser.write(b'\x34')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x42, 0)
		ser.write(b'\x42')
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [52, 1, 0, 0, 7, 0, 0, 0, 7, 0, 66, 0 ])
		ser.write(a);
		time.sleep(.01)


		ask = ser.read(1)
		print(ask)
		if (ask):
			print("Bill Habilitado",ask)
			if(ask==b'\x00'):
				time.sleep(.09)
				ESTADO_BILLETERO = 1
				return ask
				break
			else:
				if iniciarTemporizador(TON_02):
					ESTADO_BILLETERO = 0
					break
		else:
			if iniciarTemporizador(TON_02):
				ESTADO_BILLETERO = 0
				break




def enable_sequence2(ser):
		#STAKER
	print("Stacker")
	while(1):
		ser.limpiar()
		#ser.flushInput()

		"""
		time.sleep(.09)
		ser.parity = change_parity(0x36, 1)
		ser.write(b'\x36')
		ser.parity = change_parity(0x36, 0)
		ser.write(b'\x36')
		time.sleep(.09)
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [54, 1, 54, 0])
		ser.write(a);
		time.sleep(.01)



		ask = ser.read(2)
		print(ask)
		if (ask):
			if(ask[0]==254):
				print("Pila llena")
			elif(ask[0]==00):
				print("Pila Vacia")
				"""
				time.sleep(.2)
				ser.parity = change_parity(0x00, 0)
				ser.write(b'\x00')
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				time.sleep(.01)




				break

	#Bill-type
	
	while(1):
		"""
		time.sleep(.09)
		ser.parity = change_parity(0x34, 1)
		ser.write(b'\x34')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x42, 0)
		ser.write(b'\x42')
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [52, 1, 0, 0, 7, 0, 0, 0, 7, 0, 66, 0 ])
		ser.write(a);
		time.sleep(.01)


		ask = ser.read(1)
		print(ask)
		if (ask):
			print("Bill Habilitado",ask)
			if(ask==b'\x00'):
				time.sleep(.09)
				return ask
				break



def enable_sequence3(ser):
		#STAKER
	print("Stacker")
	while(1):
		ser.limpiar()

		"""
		time.sleep(.09)
		ser.parity = change_parity(0x36, 1)
		ser.write(b'\x36')
		ser.parity = change_parity(0x36, 0)
		ser.write(b'\x36')
		time.sleep(.09)
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [54, 1, 54, 0])
		ser.write(a);
		time.sleep(.01)



		ask = ser.read(2)
		print(ask)
		if (ask):
			if(ask[0]==254):
				print("Pila llena")
			elif(ask[0]==00):
				print("Pila Vacia")
				"""
				time.sleep(.2)
				ser.parity = change_parity(0x00, 0)
				ser.write(b'\x00')
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				time.sleep(.01)




				break

	#Bill-type
	
	while(1):
		"""
		time.sleep(.09)
		ser.parity = change_parity(0x34, 1)
		ser.write(b'\x34')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x07, 0)
		ser.write(b'\x07')
		ser.parity = change_parity(0x42, 0)
		ser.write(b'\x42')
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [52, 1, 0, 0, 7, 0, 0, 0, 7, 0, 66, 0 ])
		ser.write(a);
		time.sleep(.01)


		ask = ser.read(1)
		print(ask)
		if (ask):
			print("Bill Habilitado",ask)
			if(ask==b'\x00'):
				time.sleep(.09)
				return ask
				break

def palPoll(ser,r1,r):
	global cambiaColor,total,tarifa,cambio,rep,monedas,monedasTotal,dineroTotal,avis,aux_cambio,monedasPago,sensores
	entregadas=0
	tipoMoneda=0
	valorMoneda=0
	status=""
	ruta = 0
	if (128&r1 == 0 and 64&r1 != 0):
		if(32&r1==0 and 16&r1==0):
			print("ruta: Caja")
			ruta = 1
		elif (32 & r1 == 0 and 16 & r1 != 0):
			print("ruta: Tubos")
			ruta = 2
		elif (32 & r1 != 0 and 16 & r1 == 0):
			print("ruta: Sin uso")
			ruta = 3
		elif (32 & r1 != 0 and 16 & r1 != 0):
			print("ruta: Retornada")
			ruta = 4

	else:
		if(r1==1):
			status="Escrow request --- 1"
		if(r1==2):
			status="Entregaando cambio : "+str(aux_cambio)
		if(r1==3):
			status="No credit --- 3"
		if(r1==4):
			status="Defective tube sensor --- 4"
		if(r1==5):
			status="Double arrival --- 5"
		if(r1==6):
			status="Aceptor unplugged --- 6"
		if(r1==7):
			status="Tube Jam --- 7"
		if(r1==8):
			status="Checksum Error --- 8"
		if(r1==9):
			#status=""
			ms="Coin routing Error --- 9"
		if(r1==10):
			status="Changer Busy --- 10"
		if(r1==12):
			status="Coin Jam in the acceptance path --- 12"
		if(r1==13):
			status="Posible credited coin removal --- 13"
		print(status)
		avis=status
		return
	b=8
	while (b != 0):
		if (b & r1 != 0):
			tipoMoneda+=b
		b=b>>1
	if(tipoMoneda==2):
		valorMoneda=1
		monedas[0]=monedas[0]+1
		monedasPago[0]=monedasPago[0]+1
		if ruta == 2 :
			cantidad = int(sensores.getValue('MONEDERO','moneda_1'))
			sensores.editValue('MONEDERO','moneda_1',str(cantidad+1))
		elif ruta == 1 :
			cantidad = int(sensores.getValue('MONEDERO','moneda_1_caja'))
			sensores.editValue('MONEDERO','moneda_1_caja',str(cantidad+1))
	if (tipoMoneda == 3):
		valorMoneda = 2
		monedas[1]=monedas[1]+1
		monedasPago[1]=monedasPago[1]+1
		if ruta == 2 :
			cantidad = int(sensores.getValue('MONEDERO','moneda_2'))
			sensores.editValue('MONEDERO','moneda_2',str(cantidad+1))
		elif ruta == 1 :
			cantidad = int(sensores.getValue('MONEDERO','moneda_2_caja'))
			sensores.editValue('MONEDERO','moneda_2_caja',str(cantidad+1))
	if (tipoMoneda == 4):
		valorMoneda = 5
		monedas[2]=monedas[2]+1
		monedasPago[2]=monedasPago[2]+1
		if ruta == 2 :
			cantidad = int(sensores.getValue('MONEDERO','moneda_3'))
			sensores.editValue('MONEDERO','moneda_3',str(cantidad+1))
		elif ruta == 1 :
			cantidad = int(sensores.getValue('MONEDERO','moneda_3_caja'))
			sensores.editValue('MONEDERO','moneda_3_caja',str(cantidad+1))
	if (tipoMoneda == 5):
		valorMoneda = 10
		monedas[3]=monedas[3]+1
		monedasPago[3]=monedasPago[3]+1
		if ruta == 2 :
			cantidad = int(sensores.getValue('MONEDERO','moneda_4'))
			sensores.editValue('MONEDERO','moneda_4',str(cantidad+1))
		elif ruta == 1 :
			cantidad = int(sensores.getValue('MONEDERO','moneda_4_caja'))
			sensores.editValue('MONEDERO','moneda_4_caja',str(cantidad+1))
	print("Moneda insertada: ",valorMoneda)

	#cambiaColor=1
	#print("Monedas en tubo: ",r2)
	total=total+valorMoneda
	dineroTotal=dineroTotal+valorMoneda
	monedasTotal=monedasTotal+1
	print("Monto actual: ",total)


def accept_sequence(ser):
	global tiempoBillExc,tiempoLimBill
	estado=1 	  	
	while(estado<4):
		time.sleep(.09)
		#Aceptar billete (Stack) (enviarlo hacia atras)
		if(estado==1):
			"""
			ser.parity = change_parity(0x35, 1)
			ser.write(b'\x35')
			ser.parity = change_parity(0x01, 0)
			ser.write(b'\x01')
			ser.parity = change_parity(0x36, 0)
			ser.write(b'\x36')
			"""

			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [53, 1, 1, 0, 54, 0])
			ser.write(a);
			time.sleep(.01)


			r = ser.read(10)
			print("1: ",r)
			time.sleep(.005)
			if(r==b'\x00'):
				estado=2
		#Preguntar por estado del billete (Poll)
		if(estado==2):
			#aceptarMonedas(estadoConexion)
			"""
			ser.parity = change_parity(0x33, 1)
			ser.write(b'\x33')
			ser.parity = change_parity(0x33, 0)
			ser.write(b'\x33')
			"""

			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51, 1, 51, 0])
			ser.write(a);
			time.sleep(.01)


			r = ser.read(10)
			if(r):
				print("2:",r)
				time.sleep(.05)
				aux = BitArray(r)
				if(aux.bin[0:4]=="1000"):
					ser.parity = change_parity(0x00,0)
					#ser.write(b'\x00')
					estado=3
				elif(aux.bin[0:4]=="1001"):
					ser.parity = change_parity(0x00,0)
					#ser.write(b'\x00')
					estado=3
				elif(aux.bin[0:4]=="1010"):
					ser.parity = change_parity(0x00,0)
					#ser.write(b'\x00')
					estado=3
				elif(aux.bin[0:4]=="1100"):
					ser.parity = change_parity(0x00,0)
					#ser.write(b'\x00')
					estado=3
				elif(aux.bin[0:4]=="1111"):
					estado=1

						
		if(estado==3):
			#aceptarMonedas(estadoConexion)
			"""
			ser.parity = change_parity(0x33, 1)
			ser.write(b'\x33')
			ser.parity = change_parity(0x33, 0)
			ser.write(b'\x33')
			"""

			a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [51, 1, 51, 0])
			ser.write(a);
			time.sleep(.01)


			r = ser.read(50)
			#print("Espera Otra respuesta: ",r)
			if(r):
				print("3",r)
				"""
				ser.write(b'\x00')
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				time.sleep(.01)

				if(r==b'\x00'):
					tiempoLimBill=0
					estado=4
			


def disable_coin(ser):



	while (1):
		#print("asdddd")
		"""
		ser.parity = change_parity(0x0C, 1)
		ser.write(b'\x0C')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x0C, 0)
		ser.write(b'\x0C')
		"""
		print("Deshabilitando Monedero...")
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [12, 1, 0, 0, 0, 0, 0, 0, 0, 0, 12, 0])
		#ser.close();
		#exit(0)
		ser.write(a);
		time.sleep(.01)
		r = ser.read(1)


		print(r)

		#print ("Se llego hasta aqui _ 02")
		if(r):
			if (r[0] == 0):  # Verificar la respuesta <----------
				print("Deshabilitacion de Monedas Exitosa")
				time.sleep(.005)
				break






def enable_coin(ser):
	global mona,mond
	mona=60
	mond=60
	ba = [0x0C, mona, mond]
	ckInt = checkSum(ba)
	print("vals...>>>",mona,mond,ckInt)
	#time.sleep(1)
	while (1):
		#print("asdddd")
		"""
		ser.parity = change_parity(0x0C, 1)
		ser.write(b'\x0C')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(mona, 0)
		ser.write(bytes([int(mona)]))
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(mond, 0)
		ser.write(bytes([int(mond)]))
		ser.parity = change_parity(ckInt, 0)
		ser.write(bytes([int(ckInt)]))
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [12, 1, 0, 0, mona, 0, 0, 0, mond, 0, ckInt, 0])
		ser.write(a);
		time.sleep(.01)



		#time.sleep(.05)
		r = ser.read(1)
		print(r)

		#print ("Se llego hasta aqui _ 03")
		if(r):
			if (r[0] == 0):  # Verificar la respuesta <----------
				print("Habilitacion de Monedas Exitosa")
				time.sleep(.005)
				return r
				break

def obtenerPlazaYLocalidad():
	global nom, loc
	try:
		connection = psycopg2.connect(database='CajerOk',user='postgres',password='Postgres3UMd6', host='localhost')
		#connection = psycopg2.connect(user=usuario, password=contrasenia, database=bd, host='localhost')
		with connection.cursor() as cursor:
			cursor.execute(
				' SELECT nombre_plaza,estado FROM plaza WHERE idplaza = 1')
			row = cursor.fetchone()
			if row is not None:
				print("columns: {}, {}".format(row[0], row[1]))
				nom = str(row[0])
				loc = str(row[1])
				connection.commit()
				connection.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		
		



def Init(ser):
	#RESET COIN CHANGER
	global rep,nivelDeCambio,NoCajero
	##print(ser.inWaiting())
	ser.limpiar()
	#ser.flushInput()
	rep=0
	#botones.prenderMonedero()
	time.sleep(5)
	'''
	#infile = open(rutaUsuario+"Documentos/plaza.txt", 'r')
	#c=infile.readline()
	arr=c.split(',', 1 )
	infile.close()
	obtenerPlazaYLocalidad()
	infile = open(rutaUsuario+"Documentos/NoCajero.txt", 'r')
	NoCajero=infile.readline()
	infile.close()
	'''

	while (1):
		#ser.limpiar()
		##ser.flushInput()
		"""
		ser.parity = change_parity(0x08, 1)
		ser.write(b'\x08')
		ser.parity = change_parity(0x08, 0)
		ser.write(b'\x08')
		"""
		
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [8, 1, 8, 0])
		#ser.escribir(a)
		#time.sleep(0.1)


		ser.write(a);
		time.sleep(.01)

		
		r = ser.read(1)
		print("RE,",r)
		if(r):
			if (r[0] == 0):
				break
	
	ser.limpiar()
	while (1):
		"""
		ser.parity = change_parity(0x0F, 1)
		ser.write(b'\x0F')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x0F, 0)
		ser.write(b'\x0F')
		"""
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 0, 0, 15, 0])
		ser.write(a);
		time.sleep(.1)

		r = ser.read(33)  # Verificar en el simulador se ve que devuelve 34
		print(r)
		if (r):
			#print(r[0])
			if (r[0] == 77):  # Verificar la respuesta (4D = M, 45 = E, 49 = I) <----------
				"""
				ser.parity = change_parity(0x00, 0)
				ser.write(b'\x00')  # Devuelve ACK
				"""
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				time.sleep(.01)

				#print ("Se llego hasta aqui _ 01")

				break

	#ser.flushInput()
	ser.limpiar()
	disable_coin(ser)
	cont=0
	while(1):
		"""
		ser.parity = change_parity(0x0F, 1)
		ser.write(b'\x0F')
		ser.parity = change_parity(0x05, 0)
		ser.write(b'\x05')
		ser.parity = change_parity(0x14, 0)
		ser.write(b'\x14')
		"""
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 5, 0, 20, 0])
		ser.write(a);
		time.sleep(.01)


		#time.sleep(.02)
		r = ser.read(2)
		if(r):
			print("rrrrr__:",r)
			if(cont==2):
				print("LISTO!---")
				break
			else:
				cont=cont+1
				print("DESHINIBIENDO!---",cont)
				enable_coin(ser)
				time.sleep(2)
	




'''
def calcularCambio(ser):
	global cp,cambio,total,aux_tarifa,comienzaCambio,cajeroSuspendido,registraPago,killbill,pagado,aux_cambio
	if(cp==1):
		cambio = total - aux_tarifa
		cambio = aux_tarifa+cambio
		print("-.-.-.-.-.cancelando pago")
		registraPago=1
	else:
		cambio = total - aux_tarifa

	aux_cambio = cambio

	if (cambio > 0):
		print("hay cambio")
		imprime=1
		comienzaCambio=1
		#dineroTotal=dineroTotal+aux_tarifa
		disable_sequence(ser)
		#print(ser.inWaiting())
		ser.limpiar()
		#ser.flushInput()
		#ESTATUS TUBOS
		if(cajeroSuspendido==1):
			registraPago=1
			killbill = 1
			pagado=2
			
		else:

			cambioRestante = solicitarCambio(cambio)
			cambio = cambioRestante
			print("Cambio Restante: ",cambioRestante,cambio)
			#count(ser,0)
			#killbill = 1
			#pagado=2
			



	if(cambio==0): # if(total==aux_tarifa):
		imprime=1
		killbill = 1
		comienzaCambio=1
		time.sleep(.05)
		pagado=2
		if(cp==1):
			print("Pago cancelado")
			#cp=0
		else:
			registraPago=1
		#disable_coin(ser)
		disable_sequence(ser)
'''


def solicitarCambio(cambioSolicitado):
	#cambioSolicitado = 177
	
	
	#cambio5 = int(cambioSolicitado/5)
	#cambio1 = int(cambioSolicitado/1)
	cambioEntregado10 = 0
	cambioEntregado5 = 0
	cambioEntregado1 = 0
	monedasDispensadas = 0
	estatus = 0
	
	HOPPER_MONEDAS_SOLICITADAS = {10:0,5:0,1:0}
	HOPPER_MONEDAS_DISPENSADAS = {10:0,5:0,1:0}
	#MONEDAS = [10,5,1]
	MONEDAS = [10,5]
	
	cambioRestante = cambioSolicitado
	#MONEDAS = HOPPER_MONEDAS_HABILITADAS_HOPPER.keys()
	i = 0
	print("------------- Cambio Solicitado: ",cambioSolicitado,"-------------------")
	for moneda in MONEDAS:
		repeticiones = MONEDAS.count(moneda)
		i = i +1 
		#print("reps: ",repeticiones, "iteracion: ", i)
		if(repeticiones > 2):

			#count(ser)
			break
			#exit(0)
			pass
		
		
		#print("Cambio Solicitado: ",cambioSolicitado)
		#print(moneda,cambio)
		cambio = int(cambioSolicitado/moneda)
		if(cambio):
			cambioSolicitado = cambioSolicitado%moneda
			print("\nMonedas solicitadas de ",moneda,": ",cambio)
			codigoCambio = cambioHopper(cambio,HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
			dispensandoCambio = 1
			#time.sleep(1)
			
			if codigoCambio == [0]:
				while(dispensandoCambio):
					time.sleep(.3)
					estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
					if estatus:
						if estatus[1]:
							#cambioRestante = (estatus[1]*moneda)+cambioSolicitado
							print("*Entrgando Cambio*",(estatus[1]*moneda)+cambioSolicitado,"Restante")
						else:
							dispensandoCambio = 0
				if estatus:
					if estatus[0]:
						monedasPorPagar = estatus[1]
						monedasDispensadas = estatus[2]
						monedasFaltantes = estatus[3]
						if monedasFaltantes:
							MONEDAS.append(moneda)
							cambioSolicitado = cambioSolicitado + (monedasFaltantes*moneda)
							#print("monedas por pagar de ",moneda,": ",monedasPorPagar)
							print("monedas enrtegadas de ",moneda,": ",monedasDispensadas)
							#HOPPER_MONEDAS_DISPENSADAS.update({moneda:monedasDispensadas})

							cambioRestante = cambioRestante - (monedasDispensadas*moneda)
							print("Cambio incompleto , faltan ",monedasFaltantes," de $",moneda, "Restante: ",cambioRestante)
							resetHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
							habilitarHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
						else:
							#print("monedas pendientes en el pago de ",moneda,": ",monedasDispensadas)
							cambioRestante = cambioRestante - (monedasDispensadas*moneda)
							print("monedas enrtegadas de ",moneda,": ",monedasDispensadas)
							#HOPPER_MONEDAS_DISPENSADAS.update({moneda:monedasDispensadas})

							print("monedas faltantes: ",monedasFaltantes," monedas",MONEDAS,"Cambio Restante:",cambioRestante)
							#HOPPER_MONEDAS_DISPENSADAS.update({})

					else: 
						print("Hopper ",HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda],"No puede dar cambio: Deshabilitado")

				else:
					print("No se pudo obtener el status")
			else:
					resetHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
					habilitarHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
					print("No se entrego el cambio, Hopper",HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda],"Deshabilitado,","Faltaron",cambio,"monedas de $",moneda)
					#cambioRestante = cambioRestante+(cambio*moneda)


			#-------------VERIFICACION FINAL DEL STATUSHOPPER ---------------
			

			'''
			estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
			print("ultima moneda: ",moneda,cambioSolicitado,estatus,estatus[1],cambioSolicitado)
			if estatus:
				if estatus[3]:
					cambioRestante = (estatus[3]*moneda)+cambioSolicitado
					resetHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
					habilitarHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
					print("Cambio restante...: ",cambioRestante,"Reiniciando hopper")
				else:
					if estatus[0]:

						cambioRestante = (estatus[3]*moneda)+cambioSolicitado
						print("Cambio restante...: ",cambioRestante,"est0")
						pass
					else:
						print("Cambio restante...: ",cambioRestante,"Reiniciando")
						resetHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
						habilitarHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[moneda])
			'''


			print("Cambio restante...: ",cambioRestante)


			
	print("Cambio restante: ",cambioRestante)
	return cambioRestante






	#exit(0)
	"""
	cambio10 = int(cambioSolicitado/10)
	if(cambio10):
		cambioSolicitado = cambioSolicitado%10
		cambioHopper(cambio10,HOPPER_MONEDAS_HABILITADAS_HOPPER[10])
		print("monedas solicitadas de 10:",cambio10)
		estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[10])
		if estatus:
			monedasDispensadas = estatus[1]
			monedasFaltantes = estatus[2]
			if monedasFaltantes:
				print("Cambio incompleto , faltan ",monedasFaltantes," monedas")
			else:
				print("monedas enrtegadas de 10: ",monedasDispensadas)
		else:
			print("No se pudo obtener el status")


	cambio5 = int(cambioSolicitado/5)
	if(cambio5):
		cambioSolicitado = cambioSolicitado%5
		cambioHopper(cambio5,HOPPER_MONEDAS_HABILITADAS_HOPPER[5])
		print("monedas solicitadas de 5:",cambio5)
		estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[5])
		if estatus:
			monedasDispensadas = estatus[1]
			monedasFaltantes = estatus[2]
			if monedasFaltantes:
				print("Cambio incompleto , faltan ",monedasFaltantes," monedas")
			else:
				print("monedas enrtegadas de 5: ",monedasDispensadas)
		else:
			print("No se pudo obtener el status")

	cambio1 = int(cambioSolicitado/1)
	if(cambio1):
		cambioSolicitado = cambioSolicitado%1
		cambioHopper(cambio1,HOPPER_MONEDAS_HABILITADAS_HOPPER[1])
		print("monedas solicitadas de 1:",cambio1)
		estatus = statusHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[1])
		if estatus:
			monedasDispensadas = estatus[1]
			monedasFaltantes = estatus[2]
			if monedasFaltantes:
				print("Cambio incompleto , faltan ",monedasFaltantes," monedas")
			else:
				print("monedas enrtegadas de 1: ",monedasDispensadas)
		else:
			print("No se pudo obtener el status")
		

	
	
	statusHopper(HOPPER_MONEDAS_HABILITADAS_HOPPER[1])
	"""


def validarCctalk(respuesta,comando, hopperId, validacionExacta):
	lenRecepcion = len(respuesta)
	HEADER_LEN = 0
	CABAECERA_LEN = 3
	CHECKSUM_LEN = 1
	respuestaDecoded = []
	codigosValidacion = [[],[0x00],[0x00],noSeriesHoppers[hopperId],[0x00],[0x00],[0x00,0x00,0x00,0x00]]
	#print("longitud recepcion", lenRecepcion)
	if(lenRecepcion >= 2):
		numDatos = respuesta[1]
		if(numDatos >= 1):
			HEADER_LEN = 1
	else:
		print("Respuesta no valida: ", respuesta)
		return -1

	if(lenRecepcion == CABAECERA_LEN + len(codigosValidacion[comando]) + HEADER_LEN + CHECKSUM_LEN):

		respuesta = respuesta[:lenRecepcion-1]
		respuesta = respuesta[CABAECERA_LEN+HEADER_LEN:]
		#print("datos: ", respuesta)
		HEADER_LEN = 0
		for elem in respuesta:
			respuestaDecoded.append(elem)
		#print("respuestaDec / validacion ", respuestaDecoded, codigosValidacion[comando])

		if(respuestaDecoded == codigosValidacion[comando]):
			print("Datos validos: ",respuestaDecoded)
			return respuestaDecoded
		elif(not validacionExacta):
			if(len(codigosValidacion[comando]) == len(respuestaDecoded)):
				print("Datos validos CNE: ",respuestaDecoded)
				return respuestaDecoded
			else:
				print("Datos no validos CNE: ",respuestaDecoded)
				return -1
		else:
			print("Datos NO validos: ",respuestaDecoded,)
			#exit(0)
			return -1
	else:
		print("datos malformados ",lenRecepcion,CABAECERA_LEN,len(codigosValidacion[comando]),HEADER_LEN,CHECKSUM_LEN)
		return -1



def resetHopper(hopperId):
	############### RESET POLL  #################
	resetHopper = [hopperId, 0, 1, 1]
	lenresetHopper = len(resetHopper)+1
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, resetHopper)
	ser.write(a);
	time.sleep(.1)
	r = ser.read(20) #Verificar en el simulador se ven 19
	if r:
		print("resetHopper ", lenresetHopper, "HOPPER: ", hopperId, "Data:",r , len(r))
		r = r[lenresetHopper:]
		time.sleep(.01)
		validarCctalk(r,HOPPER_RESET,hopperId,VALIDACION_EXACTA)


def statusHopper(hopperId):

	############### RESET POLL  #################
	statusHopper = [hopperId, 0, 1, 166] 
	lenstatusHopper = len(statusHopper)+1
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, statusHopper)
	ser.write(a);
	time.sleep(.1)
	r = ser.read(20) #Verificar en el simulador se ven 19
	if r:
		#print("statusHopper ", lenstatusHopper, "HOPPER: ", hopperId)
		r = r[lenstatusHopper:]
		
		time.sleep(.01)
		estatus = validarCctalk(r,HOPPER_STATUS,hopperId,VALIDACION_INEXACTA)
		#print("Estatus Hopper ",hopperId,": ",estatus)
		return estatus



def habilitarHopper(hopperId):
	############### SIMPLE POLL  #################
	estado = 0
	
	if(estado == 0):
		simplePoll = [hopperId, 0, 1, 254]
		lensimplePoll = len(simplePoll)+1
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, simplePoll)
		ser.write(a);
		time.sleep(.1)
		r = ser.read(20) #Verificar en el simulador se ven 19
		print("simplePoll ", lensimplePoll, "HOPPER: ", hopperId)
		if r:
			r = r[lensimplePoll:]
			
			time.sleep(.01)
			validarCctalk(r,HOPPER_POLL,hopperId,VALIDACION_EXACTA)
			estado = 1

	############### ENABLE HOPPER  #################
	if(estado == 1):
		hopperEnable = [hopperId, 1, 1, 164, 165]
		lenhopperEnable = len(hopperEnable)+1
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, hopperEnable)
		ser.write(a);
		time.sleep(.1)
		r = ser.read(20) #Verificar en el simulador se ven 19
		if r:
			print("hopperEnable", lenhopperEnable, "HOPPER: ", hopperId)
			r = r[lenhopperEnable:]

			time.sleep(.01)
			validarCctalk(r,HOPPER_ENABLE,hopperId,VALIDACION_EXACTA)
			estado = 2

	############### SERIE HOPPER  #################
	if(estado == 2):
		serieHopper = [hopperId, 0, 1, 242]
		lenserieHopper = len(serieHopper)+1
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, serieHopper)
		ser.write(a);
		time.sleep(.1)
		r = ser.read(20) #Verificar en el simulador se ven 19
		if r:
			print("serieHopper", lenserieHopper, "HOPPER: ", hopperId)
			r = r[lenserieHopper:]
			time.sleep(.01)
			validarCctalk(r,HOPPER_SERIE,hopperId,VALIDACION_EXACTA)
			return 1


def cambioHopper(cambioSolicitado, hopperId):
	
	############### ENABLE HOPPER  #################
	#03 04 01 A7 8F BA 20 02 
	#05 04 01 A7 0A 8E 20 02
	serieHopper = noSeriesHoppers[hopperId]
	dispenseHopper = [hopperId, 4, 1, 167, serieHopper[0], serieHopper[1], serieHopper[2], cambioSolicitado]
	lendispenseHopper = len(dispenseHopper)+1
	dispenseHopper = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, dispenseHopper)
	ser.write(dispenseHopper);
	#time.sleep(.01)
	time.sleep(.1)
	r = ser.read(20) #Verificar en el simulador se ven 19
	if r:
		#print("longitud comando ", lendispenseHopper)
		r = r[lendispenseHopper:]
		#time.sleep(.01)
		validacion = validarCctalk(r,HOPPER_DISPENSE,hopperId,VALIDACION_EXACTA)
		return validacion


	#cambioSolicitado = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, [3, 0, 1, 254])
	#cambioSolicitado = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.CCTALK_DATOS, [3, 0, 1, 254])

def cambioRecicladorMonedas(cambioSolicitado):
	cambioSolicitado = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [10, 1, 10, 0])

def cambioRecicladorBilletes(cambioSolicitado):
	cambioSolicitado = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [10, 1, 10, 0])
	


def estatusTubos(ser):
	#ESTATUS TUBOS
	global MONEDAS_POR_SW,suspenderCajero,cajeroSuspendido
	TUBOS = [0,0,0,0]
	TON = Temporizador("estatusTubos", 6)
	while(1):
		TON.actualizar()
		ser.limpiar()
		tuboVacio = 0
		time.sleep(.1) #Para completar los 500 ms
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [10, 1, 10, 0])
		ser.write(a);
		time.sleep(.01)
		r = ser.read(18) #Verificar en el simulador se ven 19
		print("estatusTubos",r)
		if(len(r)>8):
			print("h", r[4],r[5],r[6],r[7],r)
			TUBOS[0] = r[4]
			TUBOS[1] = r[5]
			TUBOS[2] = r[6]
			TUBOS[3] = r[7]



			if (r[0] == 0):  # Verificar la respuesta <----------
				if(r.__sizeof__()>=30):
					for i,tubo in enumerate(TUBOS):
						if tubo == 0 and MONEDAS_HABILITADAS_MDB[i] == 1:
							#print("tubo: ",i,"cantidad:",tubo,"Habilitado:",MONEDAS_HABILITADAS_MDB[i])
							tuboVacio = 1
							if(tubo<20):
								nivelDeCambio=1
							if(tubo<10):
								nivelDeCambio=1
								#suspenderCajero=1

					#if((r[4] == 0 and MONEDAS_HABILITADAS_MDB[0]) or (r[5] == 0 and MONEDAS_HABILITADAS_MDB[1]) or (r[6] == 0 and MONEDAS_HABILITADAS_MDB[2]) or (r[7] == 0 and MONEDAS_HABILITADAS_MDB[3])):
					if tuboVacio:
						print("errinfo...")
						if iniciarTemporizador(TON):
							suspenderCajero = 1
							cs2=0
							return TUBOS
						
						'''
						suspenderCajero=1
						if(cajeroSuspendido==1):
							suspenderCajero=0
							cs2=0
							return TUBOS
						'''


					else:
						TON.entrada = 0
						TON.actualizar()
						#suspenderCajero=0
						cs2=0
						#cajeroSuspendido=0
						print("Estatus de Llenado de Tubo: ", r[0], r[1]) #Verificar si se debe imprimir en Decimal o Ascii
						mm1=r[4]
						mm2=r[5]
						mm3=r[6]
						mm4=r[7]

						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);
						return TUBOS			
				
		else:
			if iniciarTemporizador(TON):
				suspenderCajero = 1
				return TUBOS



def count(ser, estadoConexion):
	global guardar,FALTANTE,cambio_faltante,CobroFinalizado,MONEDAS_POR_SW,MONEDAS_POR_HW,registraPago,comienzaCobro,comienzaCambio,Sinpago,DA,costillo,cajeroSuspendido,cs2,suspenderCajero,cp,total,bill,cambio,tarifa,aux_cambio,killbill,pagado,monedas,monedasTotal,dineroTotal,nivelDeCambio,imprime,monedasPago,billetesPago,NoCajero,tarifasAplicadas,fechaAMD,fo,pe,h,monedasCambio
	i=-1
	#DA=DA+costillo
	descripcionMonedas=""
	descripcionBilletes=""
	descripcionMonedasCambio=""
	estatus_cambio = 0
	CODIGO_ERROR = 0
	
	comienzaCobro=1
	registraPago=0
	if(cp==1):
		cambio = total - aux_tarifa
		cambio=aux_tarifa+cambio
		print("-.-.-.-.-.cancelando pago")
	else:
		cambio = total - aux_tarifa
	aDar=0
	desconteo=0
	aux_cambio = cambio
	mm1=0
	mm2=0
	mm3=0
	mm4=0
	mmc=0
		
	if (cambio > 0):
		cambioRestante = solicitarCambio(cambio)
		cambio = cambioRestante
		print("Cambio Restante: ",cambioRestante,cambio)

	if (cambio > 0):
		print("hay cambio")
		imprime=1
		comienzaCambio=1
		time.sleep(1)
		#dineroTotal=dineroTotal+aux_tarifa
		disable_sequence(ser)
		'''#print(ser.inWaiting())
		ser.limpiar()
		#ser.flushInput()'''
		
		'''
			Modificacion cambio_01: limpiar el puerto
		'''
		ser.limpiar()
		'''
			Modificacion cambio_01: limpiar el puerto
		'''

		MONEDAS_TMP = estatusTubos(ser)
		guardar.print("Tubos antes del cambio: ",MONEDAS_TMP)
		#print("Monedas previo al cambio: ",MONEDAS_TMP)

		if(suspenderCajero==1):
			registraPago=1
			killbill = 1
			
			
		else:
			while(1):
				'''
					Modificacion cambio_01: limpiar el puerto
				'''
				ser.limpiar()
				'''
					Modificacion cambio_01: limpiar el puerto
				'''
				if(cambio<=20):
					#pagado=1
					if(cambio!=0):
						darCambio(ser,cambio)
					killbill = 1
					
					break
				else:
					darCambio(ser,20)
					cambio=cambio-20

				


			#print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nOK\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
			time.sleep(2)
			MONEDAS_POR_HW = estatusTubos(ser)
			guardar.print("Tubos despues del cambio: ",MONEDAS_POR_HW)
			#print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nOK2\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n",cajeroSuspendido)

			MONEDAS_TMP[0] = MONEDAS_TMP[0] - MONEDAS_POR_HW[0]
			MONEDAS_TMP[1] = MONEDAS_TMP[1] - MONEDAS_POR_HW[1]
			MONEDAS_TMP[2] = MONEDAS_TMP[2] - MONEDAS_POR_HW[2]
			MONEDAS_TMP[3] = MONEDAS_TMP[3] - MONEDAS_POR_HW[3]
			
			#print("Monedas dispensadas como cambio: ",MONEDAS_TMP)
			monedasCambio = MONEDAS_TMP
			
			MONEDAS_POR_SW[0] = MONEDAS_POR_SW[0] - MONEDAS_TMP[0]
			MONEDAS_POR_SW[1] = MONEDAS_POR_SW[1] - MONEDAS_TMP[1]
			MONEDAS_POR_SW[2] = MONEDAS_POR_SW[2] - MONEDAS_TMP[2]
			MONEDAS_POR_SW[3] = MONEDAS_POR_SW[3] - MONEDAS_TMP[3]
			
			
			
			
			
		if(cp==1):
			print("Pago canceladoA")
			#cp=0
		else:
			registraPago=1
	#print("1111cp",cp," registrapago-",registraPago,"CAMBIO...",cambio)
	if(cambio==0): # if(total==aux_tarifa):
		imprime=1
		killbill = 1
		comienzaCambio=1
		time.sleep(.05)
		#pagado=2
		if(cp==1):
			print("Pago cancelado")
			#cp=0
			
		else:
			registraPago=1
		#disable_coin(ser)
		disable_sequence(ser)


	if registraPago or cp:
		print("Iniciando secuencia de registro Registrar:{0}  Cancelar{1}".format(str(registraPago),str(cp)))
		"""
		Se obtiene los datos de la operacion para su registro
		"""
		datosOperacion=str(fo) + "," + str(pe) + "," + fechaAMD +" "+h
		datosOperacionBD=str(fo) + "," + str(pe) + "," + "'"+str(fechaAMD)+" "+str(h)
		descripcionMonedas = obtenerDescripcion(monedasPago)
		descripcionBilletes = obtenerDescripcion(billetesPago)
		descripcionMonedasCambio = obtenerDescripcion(monedasCambio)
		cambio_faltante = compararCambio(monedasCambio,aux_cambio)
		print("Datos Operacion: ",datosOperacion)
		print("Monto cobrado: ",aux_tarifa)
		print("Monedas recibidas: ",descripcionMonedas)
		print("Billetes recibidos: ",descripcionBilletes)
		print("Cambio solicitado: ",aux_cambio)
		print("Cambio entregado (Monedas): ",descripcionMonedasCambio)
		print("Cambio entregado (Billetes): ","0:0")

		guardar.print("Datos Operacion: ",datosOperacion)
		guardar.print("Monto cobrado: ",aux_tarifa)
		guardar.print("Monedas recibidas: ",descripcionMonedas)
		guardar.print("Billetes recibidos: ",descripcionBilletes)
		guardar.print("Cambio solicitado: ",aux_cambio)
		guardar.print("Cambio entregado (Monedas): ",descripcionMonedasCambio)
		guardar.print("Cambio entregado (Billetes): ","0:0")

		#cambio_faltante = 3
		if(cambio_faltante):
			print("Cambio incompleto, falto: ",cambio_faltante)
			print("Intentando dispensar faltante: ","0:0")
			guardar.print("Cambio incompleto, falto:",str(cambio_faltante))
			guardar.print("Monto cobrado: ",aux_tarifa)




			CODIGO_ERROR = 1
		else:
			print("Operacion exitosa.",cambio_faltante)
			CODIGO_ERROR = 0
		


		if registraPago:
			if not cambio_faltante :
				if not suspenderCajero:
					CODIGO_ERROR = OP_EXITOSA
					print("CODIGO_ERROR: Operacion registrada y completada sin incidencias",CODIGO_ERROR)
				else:
					CODIGO_ERROR = OP_EXITOSA_SUSPENDIDO
					print("CODIGO_ERROR: Operacion registrada y completada, cajero suspendido",CODIGO_ERROR)
			else:
				if not suspenderCajero:
					##### --------------------------- Correccion suspension ------------------------------- 
					#suspenderCajero = 1
					FALTANTE.pop(0)
					FALTANTE.append(str(fo)+","+str(cambio_faltante))
					##### --------------------------- Correccion suspension ------------------------------- 
					CODIGO_ERROR = OP_CAMBIO_INCOMPLETO
					print("CODIGO_ERROR: Operacion registrada, cambio incompleto",CODIGO_ERROR, cambio_faltante)
				else:
					CODIGO_ERROR = OP_CAMBIO_INCOMPLETO_SUSPENDIDO
					print("CODIGO_ERROR: Operacion registrada, cambio incompleto, cajero suspendido",CODIGO_ERROR, cambio_faltante)
			
			#REGISTRAR PAGO EN SERVIDOR
			#idcaj,mediopago,monto, descripcion de las monedas pagadas, descripcion de los billetes pagados, tarifas implementadas
			registrarPagoActual(cp, NoCajero, aux_cambio, aux_tarifa, costillo, datosOperacionBD, estadoConexion, descripcionMonedas, descripcionBilletes, descripcionMonedasCambio, 0, CODIGO_ERROR)

			
		else:
			if not cambio_faltante :
				if not suspenderCajero:
					CODIGO_ERROR = OP_CANCELADA
					print("CODIGO_ERROR: Operacion cancelada y completada sin incidencias",CODIGO_ERROR)
				else:
					CODIGO_ERROR = OP__CANCELADA_SUSPENDIDO
					print("CODIGO_ERROR: Operacion cancelada y completada, cajero suspendido",CODIGO_ERROR)

			else:
				if not suspenderCajero:
					CODIGO_ERROR = OP_CANCELADA_CAMBIO_INCOMPLETO
					##### --------------------------- Correccion suspension ------------------------------- 
					#suspenderCajero = 1
					FALTANTE.pop(0)
					FALTANTE.append(str(fo)+","+str(cambio_faltante))
					##### --------------------------- Correccion suspension ------------------------------- 
					print("CODIGO_ERROR: Operacion cancelada, cambio incompleto",CODIGO_ERROR)

				else:
					CODIGO_ERROR = OP_CANCELADA_CAMBIO_INCOMPLETO_SUSPENDIDO
					print("CODIGO_ERROR: Operacion cancelada, cambio incompleto, cajero suspendido",CODIGO_ERROR)

					
					
			
			print("ids: ",aux_tarifa,aux_cambio)
			registrarPagoActual(cp, NoCajero, aux_cambio, aux_tarifa, costillo, datosOperacionBD, estadoConexion, descripcionMonedas, descripcionBilletes, descripcionMonedasCambio, 0, CODIGO_ERROR)
		

		pagado=2
		CobroFinalizado = 1
		
		monedasPago[0]=0
		monedasPago[1]=0
		monedasPago[2]=0
		monedasPago[3]=0
		billetesPago[0]=0
		billetesPago[1]=0
		billetesPago[2]=0
		billetesPago[3]=0
		monedasCambio[0]=0
		monedasCambio[1]=0
		monedasCambio[2]=0
		monedasCambio[3]=0
		tarifasAplicadas=""
		print("",DA,"cp",cp," registrapago-",registraPago)
	

def registrarBoleto(NoCajero, aux_cambio, aux_tarifa, costillo, datosOperacionBD, estadoConexion, descripcionMonedas, descripcionBilletes, descripcionMonedasCambio, tipo):
	if(estadoConexion):
		#REGISTRA PAGO EN BD SERVIDOR
		print("******SOLICITANDO PAGO AL SERVIDOR*******      ",datosOperacion)
		#mensaje=str(NoCajero)+";"+"1"+";"+str(aux_tarifa)+";"+descripcionMonedas+";"+descripcionBilletes+";"+tarifasAplicadas
		if(tarifasAplicadas==""):
			tarifasAplicadas="13"
			
def registrarPagoActual(cp, NoCajero, aux_cambio, aux_tarifa, costillo, datosOperacionBD, estadoConexion, descripcionMonedas, descripcionBilletes, descripcionMonedasCambio, tipo, CODIGO_ERROR):
	global guardar
	print("Solocitando registro del pago ",datosOperacionBD)
	respuestaServidor = 0
	if(estadoConexion):
		#REGISTRA PAGO EN BD SERVIDOR
		#mensaje=str(NoCajero)+";"+"1"+";"+str(aux_tarifa)+";"+descripcionMonedas+";"+descripcionBilletes+";"+tarifasAplicadas
		tarifasAplicadas="13"			
		#mensaje=str(NoCajero)+";"+"1"+";"+str(costillo)+";"+str(DA)+";"+descripcionBilletes+";"+descripcionMonedasCambio+";"+str(tarifasAplicadas)
		mensaje=str(NoCajero)+";"+"1"+";"+str(costillo)+";"+str(descripcionMonedas)+";"+descripcionBilletes+";"+descripcionMonedasCambio+";"+str(tarifasAplicadas)
		print("Mensaje pago: ,tarifasAplicadas ",mensaje,tarifasAplicadas)
		if(cp):
			print("Pago cancelado")
		else:
			respuestaServidor=Servidor.configSocket("pago boleto", datosOperacionBD+"*"+mensaje)
			if(respuestaServidor==-1):
				#Sinpago=Sinpago+1
				pass
			#s.send("1;1;20.00;2:5,1:10;0:0;2,5".encode('utf-8'))
	else:
		print("Registrado sin conexion",datosOperacionBD)
		respuestaServidor = 0
		
	try:
		#REGISTRA PAGO EN BD INTERNA
		fechaAMD = time.strftime("%Y-%m-%d %H:%M:%S")
		print(fechaAMD,type(fechaAMD))
		datosOperacionBD=str(fo) + "," + str(pe) + "," + "'"+str(fechaAMD)
		consu="insert into \"PAGOS\"(\"idBoleto\",expedidora,\"fechaExpedicion\",codigo,registrado,monto,cambio,monedas,billetes, cambio_entregado, tipo) values("+datosOperacionBD+"'"+","+str(CODIGO_ERROR)+","+str(respuestaServidor)+","+str(aux_tarifa)+","+str(aux_cambio)+",'"+str(descripcionMonedas)+"','"+str(descripcionBilletes)+"','"+str(descripcionMonedasCambio)+"',"+str(0)+")"
		cur.execute(consu)
		conn.commit()
		print("Se registro el pago en BD interna. ",datosOperacionBD,str(CODIGO_ERROR))
		guardar.print("Registro interno exitoso",datosOperacionBD,str(CODIGO_ERROR))
		
	except:
		print("Error con la BD interna.")
		guardar.print("Registro interno fallido",datosOperacionBD,str(CODIGO_ERROR))
		
		


	
	
	

def compararCambio(cambioEntregado,cambioSolicitado):
	'''
		Se compara el cambio
	'''
	global sensores
	valorCambio=0
	i=-1
	if(cambioEntregado[0]==0 and cambioEntregado[1]==0 and cambioEntregado[2]==0 and cambioEntregado[3]==0):
		valorCambio=0
	else:
		for item in cambioEntregado:
			
			i=i+1
			if(item!=0):
				valorCambio=valorCambio+(item*valoresMonedas[i])
				moneda = 'moneda_'+str(i+1)
				print('Moneda seleccionada: ',moneda)
				cantidad = int(sensores.getValue('MONEDERO',moneda))
				sensores.editValue('MONEDERO',moneda,str(cantidad-item))
				
	print("comparativa cambio solicitado/entregado: ", cambioSolicitado,valorCambio)
	return cambioSolicitado - valorCambio
	
def obtenerDescripcion(lista):
	descripcion=""
	i=-1
	if(lista[0]==0 and lista[1]==0 and lista[2]==0 and lista[3]==0):
		descripcion="0:0"
	else:
		for item in lista:
			i=i+1
			if(item!=0):
				descripcion=descripcion+str(item)+":"+str(valoresMonedas[i])+","
	descripcion=descripcion.rstrip(',')
	return descripcion
def darCambioManual(ser,valor):
	while(1):
		time.sleep(.05)
		print(valor,"<--- aDar")
		ba = [0x0D, int(valor)]
		ckInt = checkSum(ba)

		"""
		ser.parity = change_parity(0x0D, 1)
		ser.write(b'\x0D')
		ser.parity = change_parity(int(valor), 0)
		ser.write(bytes([int(valor)]))
		ser.parity = change_parity(int(ckInt), 0)
		ser.write(bytes([int(ckInt)]))

		time.sleep(.05)
		ser.parity = change_parity(0x0B, 1)
		ser.write(b'\x0B')
		ser.parity = change_parity(0x0B, 0)
		ser.write(b'\x0B')
		time.sleep(.005)
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [13, 1, valor, 0, ckInt, 0])
		ser.write(a);
		time.sleep(.01)

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
		ser.write(a);
		time.sleep(.01)



		k = ser.read(4)
		if(k):
			print(k)
			if(k.__sizeof__()==18):
				if(k[0]==2):
					print("insistir",k)
					break
			if(k.__sizeof__()==19):
				if(k[0]==2 or k[1]==2):
					print("insistir",k)
					break
			if(k.__sizeof__()==20):
				if(k[0]==2 or k[1]==2 or k[2]==2):
					print("insistir",k)
					break
	while(1):
		"""
		ser.parity = change_parity(0x0B, 1)
		ser.write(b'\x0B')
		ser.parity = change_parity(0x0B, 0)
		ser.write(b'\x0B')
		time.sleep(.005)
		"""
		self.ser.limpiar()
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
		ser.write(a);
		time.sleep(.01)


		k = ser.read(3)
		print("poll",k)
		if(k):
			if(k[0]==0):
				print("roto")
				time.sleep(.005)
				break


def darCambio(ser,monto):
	TON_01 = Temporizador("dar cambio", 9)
	TON_02 = Temporizador("dar canbio 2", 9)
	ser.limpiar()
	ser.limpiar()
	while(1):
		print("NO")
		global total,cambio
		#print(monto)
		dar=monto/factorDeEscala
		print(dar)
		ba = [0x0F, 0x02, int(dar)]
		ckInt = checkSum(ba)
		#print("cambio->", cambio, "check->", ckInt)


		"""
		ser.parity = change_parity(0x0F, 1)
		ser.write(b'\x0F')
		ser.parity = change_parity(0x02, 0)
		ser.write(b'\x02')
		ser.parity = change_parity(int(dar), 0)
		ser.write(bytes([int(dar)]))
		ser.parity = change_parity(int(ckInt), 0)
		ser.write(bytes([int(ckInt)]))
		time.sleep(.009)
		ser.parity = change_parity(0x0B, 1)
		ser.write(b'\x0B')
		ser.parity = change_parity(0x0B, 0)
		ser.write(b'\x0B')
		time.sleep(.005)
		"""
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [15, 1, 2, 0, int(dar), 0, int(ckInt), 0])
		ser.write(a);
		time.sleep(.01)
		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
		ser.write(a);
		time.sleep(.01)
		k = ser.read(3)
		if(k):
			print(k)
			if(len(k) >= 2):

				if(k[0]==2 or k[1]==2):
					print("Comenzando pago..",k)
					#ESTADO_BILLETERO = 1
					break



				else:
					if iniciarTemporizador(TON_01):
						#ESTADO_BILLETERO = 0
						break
		else:
			if iniciarTemporizador(TON_01):
				#ESTADO_BILLETERO = 0
				break


	while(1):
		"""
		ser.parity = change_parity(0x0B, 1)
		ser.write(b'\x0B')
		ser.parity = change_parity(0x0B, 0)
		ser.write(b'\x0B')
		time.sleep(.005)
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [11, 1, 11, 0])
		ser.write(a);
		time.sleep(.01)

		k = ser.read(6)
		print("poLL",k)
		if(k):
			if(k[0]!=2):
				palPoll(ser,k[0], k)
				if(k[0]==0):
					print("roto")
					time.sleep(.005)
					break
				else:
					#ser.flushOutput()
					#ser.flushInput()
					print("Error al finalizar el pago...")

					"""
					ser.parity = change_parity(0x00, 0)
					ser.write(b'\x00')
					"""
					a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
					ser.write(a);
					time.sleep(.01)
					if iniciarTemporizador(TON_02):
						a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
						ser.write(a);
						#ESTADO_BILLETERO = ESTADO_DESHABILITADO
						break
					
		else:
			if iniciarTemporizador(TON_02):
				a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [0, 0])
				ser.write(a);
				#ESTADO_BILLETERO = ESTADO_DESHABILITADO
				break



			#if(k[0]==0):
			#	break;


def change_parity(comando,paridad):
	b=128
	cont=0
	while b!=0 :
		if b&comando!=0:
			cont=+cont+1
		b=b>>1
	if paridad == 1:
		if cont % 2 == 0:
			return serial.PARITY_ODD
		else:
			return serial.PARITY_EVEN
	elif paridad == 0:
		if cont % 2 == 0:
			return serial.PARITY_EVEN
		else:
			return serial.PARITY_ODD

def checkSum(arr):
	j=0
	sum=0
	tam=arr.__len__()
	while(j<tam):
		#print(j, tam)
		sum=sum+arr[j]
		print(sum)
		j=j+1	
	return 255&sum



def clicks():
	#Leyendo stream de video...
	time.sleep(5)
	time.sleep(10)
	print("Click 11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
	os.system("xdotool click 1")
	time.sleep(3)


def streaming():
	#Leyendo stream de video...
	time.sleep(5)
	time.sleep(8)
	print("Click 0000000000000000000000000000000000000000000000000000000000000000000000000000000000")
	os.system("xdotool click 1")
	#time.sleep(8)
	try:
		os.system("mpv --fs --fs-screen=2 --quiet --loop-playlist yes --playlist Vídeos/")
		time.sleep(3)
		os.system("xdotool click 1")
		print("Click 111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111")
	except:
		print("error en el stream")
	time.sleep(5)
	time.sleep(3)
	print("Click 22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222")
	os.system("xdotool click 1")
	time.sleep(3)



def leerCodQR2():
	global camInicial
	#time.sleep(1)
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
				#print('Camara Detectada')
				lee = os.system("zbarcam --raw --prescale=280x150   "+cam+" > /home/cajero/Documentos/ticket.txt")
				#lee = os.system("zbarcam --raw  --prescale=10x10 /dev/video0 >ruta+ ../../app/caseta/ticket.txt")
				#lee = os.system(ruta+"../../app/caseta/dsreader -l 27 -b 14 -r 30 -s 100 -u 50  >ruta+ ../../app/caseta/ticket.txt")
				#lee = os.system("cd /home/cajero/scanner/dsreader")
				#lee = os.system("./dsreader -l 27 -b 14 -r 30 -s 100 -u 50  >ruta+ ../../app/caseta/ticket.txt")

			except e:
				mensajeTolerancia=1
				#print("Error al crear el socket: ",e)
		else:
			
			if(cam!=''):
				camInicial=cam
			else:
				#print('Camara desconectada')
				pass


def reiniciarComuicacion():
	global ser
	#STAKER
	print("RESET SERIAL")
	TON_02 = Temporizador("RESET ARDUINO", 4)
	a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.RESET)
	ser.write(a);
	while(1):
		TON_02.entrada = not TON_02.salida
		TON_02.actualizar()
		print("tiempo transcurrido: ",TON_02.tiempoActual,TON_02.salida,TON_02.tiempo)
		if TON_02.salida:
			print("FIN RESET")
			ser = abrirPuerto()
			return 1




def disable_sequence(ser):
#Bill-type-
	print("Bill-Type-disable")
	while(1):
		time.sleep(1)
		"""
		ser.parity = change_parity(0x34, 1)
		ser.write(b'\x34')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x00, 0)
		ser.write(b'\x00')
		ser.parity = change_parity(0x34, 0)
		ser.write(b'\x34')
		"""

		a = comunicacion.crearInstruccion(Comunicacion.PROCESO, Comunicacion.MDB_DATOS, [52, 1, 0, 0, 0, 0, 0, 0, 0, 0, 52, 0])
		ser.write(a);
		time.sleep(.01)


		ask = ser.read(1)
		print(ask)
		if (ask):
			if(ask==b'\x00'):
				time.sleep(.25)
		break


def iniciarTemporizador(TON):

	TON.entrada = True
	TON.actualizar()
	print("tiempo transcurrido: ",TON.tiempoActual,TON.salida,TON.tiempo)
	if TON.salida:
		print("secuencia no completada: ",TON.nombre)
		return True
	else:
		return False
			
		

def abrirPuerto():
	global ser
	ser = serial.Serial(obtenerNombreDelPuerto(dispositivo = Botones.PUERTO_ARDUINO_MICRO))  # Open named port
	ser.baudrate = 9600  # Set baud rate
	ser.parity = serial.PARITY_NONE
	ser.stopbits = serial.STOPBITS_ONE
	ser.bytesize = serial.EIGHTBITS
	#ser.timeout = 0
	#ser.timeout = .005
	#ser.timeout = .005 tiempo raspberry
	ser.timeout = .005
	return ser

#MAIN
if __name__ == "__main__":
	#global ser
	os.system("echo eum | sudo -S chmod 777 /dev/ttyUSB*")
	time.sleep(3)

	ba = [0x04,0x04,0x01,0xA7,0x00,0x8E,0x20,0x02]
	ckInt = checkSum(ba)
	print("checksum: ",256-(ckInt%256))

	comunicacion = Comunicacion ()
	"""
	ser = PuertoSerie ("PuertoSerie")
	ser.modificarConfiguracion (dispositivo = PuertoSerie.PUERTO_ARDUINO_MICRO, baudrate = 9600)
	ser.start()
	ser.abrirPuerto()
	"""


	#ser = abrirPuerto()
	ser = PuertoSerie ("PuertoSerie",dispositivo = PuertoSerie.ARDUINO_MICRO)
	ser.abrirPuerto()
	#reiniciarComuicacion()
	

	

	print("FIN RESET2")
	


	leerArch = open(rutaUsuario+"Documentos/ticket.txt", "w")
	leerArch.write('')
	leerArch.close()
	#pulsos = Botones("/dev/ttyUSB1", 3, 2)
	#pulsos = Botones("/dev/ttyUSB1", 3, 3, dispositivo = Botones.PUERTO_ARDUINO)
	conexion = Conexiones()
	cola = Pila()
	

	HOPPER_3 = 3
	HOPPER_4 = 4
	HOPPER_5 = 5
	HOPPER_6 = 6


	HOPPER_POLL = 1
	HOPPER_ENABLE = 2
	HOPPER_SERIE = 3
	HOPPER_DISPENSE = 4
	HOPPER_RESET = 5
	HOPPER_STATUS = 6

	ESTADO_DESHABILITADO = 0
	ESTADO_HABILITADO = 1
	HOPPER_STATUS = 6

	#HOPPER_MONEDAS_HABILITADAS_HOPPER = {10 : HOPPER_5, 5 : HOPPER_4, 1 : HOPPER_3 }
	HOPPER_MONEDAS_HABILITADAS_HOPPER = {1 : HOPPER_5, 10 : HOPPER_4, 5 : HOPPER_3 }
	

	#MONEDAS_HABILITADAS_MDB = [1,2,5,10]
	MONEDAS_HABILITADAS_MDB = [ESTADO_HABILITADO,ESTADO_HABILITADO,ESTADO_HABILITADO,ESTADO_HABILITADO]

	
	#noSeriesHoppers = [[],[],[],[0x8F,0xBA,0x20],[0x00,0x8E,0x20],[0x0A,0x8E,0x20]]
	noSeriesHoppers = [[],[],[],[0x8F,0xBA,0x20],[0x0A,0x8E,0x20],[0x00,0x8E,0x20]]

	
	VALIDACION_INEXACTA = 0
	VALIDACION_EXACTA = 1
	estadoConexion = 0
	
	#time.sleep(20)


	ESTADO_MONEDERO = ESTADO_HABILITADO
	ESTADO_BILLETERO = ESTADO_HABILITADO


	resetHopper(int(HOPPER_3))
	resetHopper(int(HOPPER_4))
	resetHopper(int(HOPPER_5))

	habilitarHopper(int(HOPPER_3))
	habilitarHopper(int(HOPPER_4))
	habilitarHopper(int(HOPPER_5))
	
	#solicitarCambio(3)
	

	
	
	test = 0
	while(test != 0):
		test = int(input("Cambio a dispensar: "))
		#print("...Dispensando: ",test)
		solicitarCambio(test)
	
	'''
	cambioHopper(0,int(HOPPER_3))
	cambioHopper(2,int(HOPPER_4))
	cambioHopper(0,int(HOPPER_5))
	'''

	Init(ser)
	#enable_coin(ser)
	disable_sequence(ser)
	#INICIALIZAMOS EL HILO DE LA INTERFAZ

	
	'''test = 1
	while(test != 0):
		test = int(input("Cambio a dispensar: "))
		#print("...Dispensando: ",test)
		solicitarCambio(test)
	'''

	

	thread1 = Thread(target=interface,args=())
	#time.sleep(5)
	thread3 = Thread(target=streaming, args = ())
	thread5 = Thread(target=clicks, args=())
	thread4 = Thread(target=leerArchivo, args=())
	
	#os.system("sudo nice -n -19 python3 archimp.py")
	try:

		thread3.start()
		time.sleep(4)
		#thread5.start()
		time.sleep(.4)
		thread1.start()
		thread4.start()
		time.sleep(5)
		os.system("xprop -f _MOTIF_WM_HINTS 32c -set _MOTIF_WM_HINTS '0x2, 0x0, 0x0, 0x0, 0x0'")
		time.sleep(10)
		os.system("xdotool click 1")
		print("Click 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333")


	except Exception as e:
		pass

	while(thread1.is_alive()):
		kill = 0
	kill = 1
	if(ser.is_open):
		ser.close()
	else:
		print("termine")
		exit(0)
	

