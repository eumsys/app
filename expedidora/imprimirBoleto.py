# -*- coding: utf-8 -*-

#from escposprinter import *#original funcional
import tratarImagen as imagen
import configuracionEXP as archivoConfiguracion
import time
#import codigoQR as codigoGenerar
import psycopg2
import signal
from usb.core import USBError
from escpos.printer import Usb


import os
import sys
import errno

usuario = 'postgres'
contrasenia = 'Postgres3UMd6'
db = 'dbeum_tecamac'

def instanciarImpresora():
	try:
		Generic = Usb(0x0519, 0x0001, timeout=400)
		return Generic
	except Exception as error:
		return "No esta conectada la impresora"

def imprimirHeader():
	nom_plaza = ""
	politicas = ""
	try:
		Generic = instanciarImpresora()
		if Generic == "No esta conectada la impresora":
			return Generic
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
		#Generic.set(size='2x', align='center')
		Generic.set(align=u'CENTER', font=u'B',width=2,height=2)
		Generic.text('Bienvenido \n'+str(nom_plaza)+'\n')
		Generic.set(align=u'center', font=u'B')
		#Generic.set(size='normal',align='center')
		palabra = ""
		for letra in politicas:
			if letra != "|":
				palabra = palabra + letra
			else:
				print(palabra)
				Generic.text(palabra)
				Generic.text(" \n")
				palabra = ""
		return "ack"
	except Exception as error:
		print(error)
		return "No se pudo imprimir"
	except TimeoutException:
		return "No se pudo imprimir"

def imprimirQR2DS(noBol,terminalEnt,fechaIn,horaEnt):
	try:
		Generic = instanciarImpresora()
		if Generic == "No esta conectada la impresora":
			return Generic
		
		Generic.text('Expedidora #'+terminalEnt+'\n')
		Generic.text('Folio:'+str(noBol)+'   '+fechaIn+' '+horaEnt +'\n')
		Generic.qr("Estacionamientos unicos de Mexico\n"+noBol+","+noBol+","+noBol+"\n"+terminalEnt+","+terminalEnt+","+terminalEnt+"\n"+fechaIn+","+fechaIn+","+fechaIn+"\n"+horaEnt+","+horaEnt+","+horaEnt)
		Generic.cut()
		print("QR bien impresa")
		return "ack"
	except Exception as error:
		print("ERROR AL IMPRIMIR QR")
		return "No se pudo imprimir"
		
def imprimirQR2(noBol,terminalEnt,fechaIn,horaEnt):
	try:
		Generic = instanciarImpresora()
		if Generic == "No esta conectada la impresora":
			return Generic
		Generic.set(align=u'center',font=u'B')
		Generic.image("/home/pi/Documents/eum/app/expedidora/logoPT.png")
		#Generic.set(align=u'left', font=u'B',width=2,height=2)
		#Generic.text('Bienvenido \n'+str("SAMS SATELITE")+'\n')
		Generic.set(align=u'center', font=u'B')
		pol="   La empresa no se hace responsable por objetos personales,\n   fallas mecanicas y/o electricas, siniestros ocasionados por\n   derrumbes, temblores, terremotos o fenomenos naturales, asi \n   como robo de accesorios o vandalismo en su vehiculo o robo \n   con violencia y portador de arma de fuego. \n  Solo por robo total de acuerdo a los terminos del seguro contratado\n   Boleto Perdido.\n   Se entregara el  vehiculo  a quien acredite la  propiedad.\n   El seguro contratado no aplica a motocicletas.\n   Costo del boleto perdido es de $150.00 \n   Al recibir este boleto acepta las condiciones del seguro contra\n   robo total. PARKING TIP S.A. de C.V. / R.F.C PTI120210571\n   Escobillera 13 Col. Paseos de Churubusco CDMX C.P 09030\n"	

		"""pol="Las dos primeras horas $5.00 con boleto sellado\n$10.00 hora o fraccion adicional\nLa empresa no se hace responsable por objetos\npersonales,fallas mecanicas  y/o  electricas,\nsiniestros ocasionados por derrumbes,temblores,\nterremotos o fenomenos naturales,asi como ro-\nbo de accesorios o vandalismo en su vehiculo.\nbo de accesorios o vandalismo en su vehiculo.\nPor robo total de acuerdo a los terminos  del\nseguro contratado.Boleto Perdido.Se entregara\nel  vehiculo  a quien acredite la  propiedad.\nEl seguro contratado no aplica a motocicletas.\nCosto del boleto perdido es de $100.00\nAl recibir este boleto acepta las condiciones\ndel seguro contra robo total. PARKING TIP S.A\nDE  C.V.  -R.F.C PTI120210571. Escobillera 13\nCol.Paseos de Churubusco Iztapalapa CDMX C.P.\n09030 Horario de Lunes-Domingo de 7 a 22 hrs\n"
"""
		Generic.text('\n'+pol)
		Generic.set(align=u'center', font=u'B')
		Generic.text('Expedidora #'+terminalEnt+'\n')
		Generic.text('Folio:'+str(noBol)+'   '+fechaIn+' '+horaEnt +'\n')
		#Generic.set(align=u'center', font=u'B')
		#Generic.qr("Estacionamientos unicos de Mexico\n"+noBol+"\n"+terminalEnt+"\n"+fechaIn+"\n"+horaEnt,ec=0,size=4)
		Generic.qr("M,"+noBol+","+terminalEnt+","+fechaIn+","+horaEnt,ec=0,size=5)
		Generic.cut()
		print("QR bien impresa")
		return "ack"
	except Exception as error:
		print("ERROR AL IMPRIMIR QR",error)
		return "No se pudo imprimir"

def footer():
	try:
		Generic = instanciarImpresora()
		if Generic == "No esta conectada la impresora":
			return Generic
		Generic.cut()
		print(e)
		return "ack"
	except Exception as error:
		return "No se pudo imprimir"

#imprime= commands.getoutput("lp -d SANEI_SK_Series /home/pi/Documents/eum/impresora/pruebas/test.pdf")
#imprimirHeader()
#imprimirQR2("28","1","07/09/2017","09:42:00")
