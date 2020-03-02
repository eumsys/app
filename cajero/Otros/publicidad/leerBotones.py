# -*- coding: utf-8 -*-
"""
Estacionamientos unicos de México
Este archivo es para remplaar a acceso4.py
Funcion: 		Funcion de leerBotones
Descripcion:	Leer los pines de la rasp e imprimir folio
				tambien validamos los bones y falta diseñar la
				señal de sos

Funciones que se pueden usar:
	1) leerBotones()
	2) validarBotones()		
	3) leerBotonesEntrada()
	4) configurarPinesGPIO()
	*) SOS()

"""
import RPi.GPIO as GPIO

import time



def configurarPinesGPIO():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26,GPIO.IN)
	#@GPIO.setup(6,GPIO.OUT)
	pass
def configurarPinesGPIOBobina():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(5,GPIO.IN)
	pass

def abrir():
	GPIO.output(13,True)
	time.sleep(0.5)
	GPIO.output(13,False)
	






def leerBotonesEntrada():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(26,GPIO.IN)
	publicidad=GPIO.input(26)
	#limpiar()
	return publicidad
	pass
	
def leerSensorMovimiento():
	sensorMovimiento=GPIO.input(16)
	return sensorMovimiento
	pass
	
def leerBotonesEntrada2():
	chapaMagnetica2=GPIO.input(26)
	return chapaMagnetica2
	pass
def validarBotones(b1,b2):
	if b1==True and b2==True:
		global contadorPresionarBoleto
		contadorPresionarBoleto=contadorPresionarBoleto+1
		return True
	else:
		return False
	pass


def limpiar():
	GPIO.cleanup()
	
def abrirPuerta():
	print("Abrir")
	GPIO.output(20,True)
	time.sleep(0.5)
	pass
	
def cerrarPuerta():
	print("Cerrar")
	GPIO.output(20,False)
	time.sleep(0.5)
	pass


contadorPresionarBoleto=0	
#leerBotones()
