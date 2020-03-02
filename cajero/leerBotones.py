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
	GPIO.setup(16,GPIO.IN)
	GPIO.setup(5,GPIO.IN)
	GPIO.setup(26,GPIO.IN)
	GPIO.setup(20,GPIO.OUT)
	GPIO.setup(27,GPIO.OUT)  #POSICION 7 EN RASP
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
	

def beep():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(18,GPIO.OUT)
	for i in range (0,1):
		for pulse in range(30):
			GPIO.output(18,True)
			time.sleep(0.001)
			GPIO.output(18,False)
			time.sleep(0.001)
		time.sleep(0.02)




def leerBotonesEntrada():
	chapaMagnetica=GPIO.input(5)
	return chapaMagnetica
	pass
	
def botonCancelar():
	bnCancelar=GPIO.input(16)
	return bnCancelar
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
	
def configurarPublicidad():
	print("CONFIGURACION DE PUB")
	GPIO.output(27,True)
	time.sleep(0.5)
	pass
	
def manteniendoElCero():
	print("CONFIGURACION DE PUB")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(27,GPIO.OUT)  #POSICION 7 EN RASP
	GPIO.output(27,False)
	time.sleep(1)
	pass
	
def prenderMonedero():
	print("CONFIGURACION DE PUB")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(12,GPIO.OUT)  #POSICION 7 EN RASP
	GPIO.output(12,True)
	#time.sleep(1)
	pass
	
def apagarMonedero():
	print("CONFIGURACION DE PUB")
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(12,GPIO.OUT)  #POSICION 7 EN RASP
	GPIO.output(12,False)
	#time.sleep(1)
	pass


contadorPresionarBoleto=0	
#leerBotones()
