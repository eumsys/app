# -*- coding: utf-8 -*-

#from escposprinter import *#original funcional
import tratarImagen as imagen
import configuracionEXP as archivoConfiguracion
import time
#import codigoQR as codigoGenerar
import psycopg2
import signal
import os
import sys
import errno

from usb.core import USBError

from escpos.printer import Usb



usuario = 'postgres'
contrasenia = 'Postgres3UMd6'
db = 'dbeum_tecamac'

PATH_NOMBRE_PLAZA=str(archivoConfiguracion.getName()).replace('\n','')
PATH_NUMERO_TERMINAL=str(archivoConfiguracion.getNumTer()).replace('\n','')
PATH_CODIGOS_QR="/home/pi/Documents/EUM_EXPE/CodigosQR/outputQR.png"


def instanciarImpresora():
	try:
		#Generic = Usb(0x0519, 0x2013, timeout=400)
		Generic = Usb(0x0519, 0x0001, timeout=400)
		#Generic = Usb(0x04b8, 0x0202, timeout=400)
		return Generic
	except Exception as error:
		return "No esta conectada la impresora"

def imprimirHeader():
	nom_plaza = ""
	politicas = ""
	try:
		connection = psycopg2.connect(user=usuario, password=contrasenia, database=db, host='localhost')
		with connection.cursor() as cursor:
			cursor.execute(' SELECT nombre_plaza FROM plaza WHERE idplaza = 1')
			row = cursor.fetchone()
			if row is not None:
				nom_plaza = str(row[0])
				connection.commit()
			else:
				print("No se encontro la plaza")
			cursor.execute(' SELECT descripcion FROM politicas WHERE idpoliticas = 1')
			row2 = cursor.fetchone()
			if row2 is not None:
				politicas = str(row2[0])
				connection.commit()
			else:
				print("No se encontraron las politicas")
			connection.close()
	except (Exception, psycopg2.DatabaseError) as error:
		print(error)
		return "No se pudo establecer conexion con la base de datos"
	try:
		Generic = instanciarImpresora()
		if Generic == "No esta conectada la impresora":
			return Generic
		Generic.set(size='2x', align='center')
		Generic.text('Bienvenido \n'+str(nom_plaza)+'\n')
		Generic.set(size='normal',align='center')
		palabra = ""
		for letra in politicas:
			if letra != "|":
				palabra = palabra + letra
			else:
				Generic.text(palabra)
				Generic.text(" \n")
				palabra = ""
		return "ack"
	except Exception as error:
		print(error)
		return "No se pudo imprimir"
	except TimeoutException:
		return "No se pudo imprimir"

def imprimirQR6():
	print("emp22")
	try:
		Generic = instanciarImpresora()
		if Generic == "No esta conectada la impresora":
			return Generic
		#Generic.text('Bienvenido \n'+str(nom_plaza)+'\n')
		Generic.image("/home/pi/Documents/eum/app/expedidora/bo.jpg")
		Generic.cut()
	except Exception as error:
		print("ERROR AL IMPRIMIR QR",error)
		return "No se pudo imprimir"
		
def imprimirQR22(noBol,terminalEnt,fechaIn,horaEnt,plaza,localidad,pol):
	print("emp")
	try:
		Generic = instanciarImpresora()
		if Generic == "No esta conectada la impresora":
			return Generic
		
		
		#Generic.text('Bienvenido \n'+str(nom_plaza)+'\n')
		Generic.set(align=u'center',font=u'B')
		Generic.image("/home/pi/Documents/eum/app/expedidora/logoPT.png")
		Generic.set(align=u'center',font=u'A', text_type=u'B', width=1, height=1)
		Generic.text('\n')		
		Generic.set(align=u'left',font=u'B')
		print("ACAAAAA",pol)
		Generic.text(str(pol))
		Generic.set(align=u'center',font=u'B')
		Generic.text('   Folio#'+str(noBol)+'   '+fechaIn+' '+horaEnt +'   Entrada:'+terminalEnt+"\n")
		content="Estacionamientos unicos de Mexico\n"+terminalEnt+noBol+"\n"+terminalEnt+"\n"+fechaIn+"\n"+horaEnt
		Generic.set(align=u'center',font=u'B')
		Generic.qr(content,ec=0,size=4)
		
		#codigoGenerar.construirCodigoEntrada(str(noBol),terminalEnt,fechaIn,horaEnt )
		#Generic.qr(content,ec=0,size=3,model=2,native=False,center=False)
		Generic.cut()
		#codQR=imagen.cambiarTamQR(PATH_CODIGOS_QR)
		#Generic.image(codQR)
		print("QR bien impresa")
		return "ack"
	except Exception as error:
		print("ERROR AL IMPRIMIR QR",error)
		return "No se pudo imprimir"
		
def  imprimirQR2(noBol,terminalEnt,fechaIn,horaEnt):
	
	Generic = instanciarImpresora()
	Generic.text('Expedidora #'+terminalEnt+'\n')
	Generic.text('Folio:'+str(noBol)+'   '+fechaIn+' '+horaEnt +'\n')
	codigoGenerar.construirCodigoEntrada(noBol,terminalEnt,fechaIn,horaEnt)
	codQR=imagen.cambiarTamQR(PATH_CODIGOS_QR)
	Generic.text('Expedidora #'+PATH_NUMERO_TERMINAL+'\n')
	Generic.text('Folio: GM'+str(noBol)+' '+fechaIn+' '+horaEnt +'\n')
	Generic.image(codQR)

def cutter():
	try:
		Generic = instanciarImpresora()
		Generic.cut()
		print("QR bien impresa")
		return "ack"
	except Exception as error:
		print("ERROR AL IMPRIMIR QR",error)
		return "No se pudo imprimir"
		
def footer():
	try:
		Generic = instanciarImpresora()
		print(Generic)
		if Generic == "No esta conectada la impresora":
			return Generic
		Generic.cut()
		print(e)
		return "ack"
	except Exception as error:
		return "No se pudo imprimir"

#imprime= commands.getoutput("lp -d SANEI_SK_Series /home/pi/Documents/eum/impresora/pruebas/test.pdf")
#imprimirHeader()
#imprimirQR6()


