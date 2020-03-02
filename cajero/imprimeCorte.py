# -*- coding: utf-8 -*-
"""
Estacionamientos unicos de México
Este archivo es para remplaar a acceso4.py
Funcion: 		Funcion de imprimir boleto
Descripcion:	

Funciones que se pueden usar:
	1) imprimirBoletoT tiempo corto formato largo
	2) imprimirBoleto  tiempo largo formato pequeño

"""
from escposprinter import *#original funcional
import tratarImagen as imagen
import configuracionEXP as archivoConfiguracion
import time

PATH_NOMBRE_PLAZA=str(archivoConfiguracion.getName()).replace('\n','')
PATH_NUMERO_TERMINAL=str(archivoConfiguracion.getNumTer()).replace('\n','')
PATH_CODIGOS_QR="/home/pi/Documents/EUM_EXPE/CodigosQR/outputQR.png"


#Generic = printer.Usb(0x0519,0x0001)
Generic = printer.Usb(0x0519,0x0001)
def imprimirBoletoC2(datosCajero):
	global Generic
	#Generic = printer.Usb(0x0519,0x0001)
	Generic.set(size='2x', align='center')
	Generic.text(str(PATH_NOMBRE_PLAZA)+'\n\n')
	Generic.set(size='normal',align='center')
	
	#Generic.text('--------------------------------\n')
	#Generic.text("La empresa no se hace responsable por objetos\npersonales,fallas mecanicas  y/o  electricas,\nsiestros ocasionados por derrumbes,temblores,\nterremotos o fenomenos naturales,asi como ro-\nbo de accesorios o vandalismo en su vehiculo.\n")
	#Generic.text("Por robo total de acuerdo a los terminos  del\nseguro contratado.Boleto Perdido.Se entregara\nel  vehiculo  a quien acredite la  propiedad.\nCosto del boleto perdido es de $100.00\n")
	#Generic.text("Al recibir este boleto acepta las condiciones\ndel seguro contra robo total. PARKING TIP S.A\nDE  C.V.  -R.F.C PTI120210571. Escobillera 13\nCol.Paseos de Churubusco Iztapalapa CDMX C.P.\n09030 Horario de Lunes-Domingo de 7 a 22 hrs \n")
	horaActual= time.strftime("%H:%M:%S")
	Generic.text('Fecha: '+datosCajero[0]+'\n'+'Hora: '+horaActual+'\n')
	Generic.set(size='normal')
	Generic.text('\nMonedas de $1: '+datosCajero[1]+'\n'+'Monedas de $2: '+datosCajero[2]+'\n'+'Monedas de $5: '+datosCajero[3]+'\n'+'Monedas de $10: '+datosCajero[4]+'\n'+'Monedas totales: '+datosCajero[5]+'\n')
	Generic.text('Billetes de $20: '+datosCajero[6]+'\n'+'Billetes de $50: '+datosCajero[7]+'\n'+'Billetes de $100: '+datosCajero[8]+'\n'+'Billetes de $200: '+datosCajero[9]+'\n'+'Billetes totales: '+datosCajero[10]+'\n')
	#Generic.text('\n--------------------------------\n')
	Generic.text('\n\nDinero total en monedas: '+datosCajero[11])
	Generic.text('\nDinero total en billetes: '+datosCajero[12])
	Generic.text('\n--------------------------------\n')
	Generic.text('Dinero total en cajero: '+datosCajero[13]+'\n\n')
	Generic.text('Cartuchos remplazados: '+datosCajero[14]+'\n\n\n')
	Generic.cut()
	
def prub():
	global Generic
	
	Generic.cut()
	
"""leerArch = open("/home/pi/Documents/reporteCorteCaja.txt", "r")
sp=leerArch.readline().split(',',14)
d1=sp[0]
d2=sp[1]
d3=sp[2]
d4=sp[3]
d5=sp[4]
d6=sp[5]
d7=sp[6]
d8=sp[7]
d9=sp[8]
d10=sp[9]
d11=sp[10]
d12=sp[11]
d13=sp[12]
d14=sp[13]
d15=sp[14]
leerArch.close()
leerArch = open("/home/pi/Documents/reporteCorteCaja.txt", "w")
leerArch.write('')
leerArch.close()
#imprimirBoletoC2(sp)"""
prub()
