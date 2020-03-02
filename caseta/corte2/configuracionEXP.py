# -*- coding: utf-8 -*-
"""
Estacionamientos unicos de México
GABRIEL MENDOZA RUIZ
Formato:
	primera linea del archivo:
		Nombre de la plaza
	segunda linea del archivo:
		Direccion (estado) de la plaza 
	tercera linea del archivo:
		Direccion (municipio) de la plaza 
	cuarta linea del archivo:
		numero de terminal
"""

PATH_ARCHIVO_CONFIGURACION_TERMINAL="/home/pi/Documents/eum/app/caseta/archivos/configuracionTerminal.txt"



def getName():
	archi = open(PATH_ARCHIVO_CONFIGURACION_TERMINAL,"r")
	nombrePlaza=archi.readline()
	archi.close()
	return nombrePlaza.replace('\n','')

def getDireccion():
	archi = open(PATH_ARCHIVO_CONFIGURACION_TERMINAL,"r")
	x=archi.readline()
	direccion1=(archi.readline()).replace('\n','')
	direccion2=(archi.readline()).replace('\n','')
	return str(direccion1)+" "+str(direccion2)

def getNumTer():
	archi = open(PATH_ARCHIVO_CONFIGURACION_TERMINAL,"r")
	x=archi.readline()
	y=archi.readline()
	z=archi.readline()
	numTer=archi.readline()
	return numTer.replace('\n','')
	archi.close()
	

def getDireccion1():
	archi = open(PATH_ARCHIVO_CONFIGURACION_TERMINAL,"r")
	x=archi.readline()
	direccion1=archi.readline()
	direccion2=archi.readline()
	return str(direccion1).replace('\n','')

def getDireccion2():
	archi = open(PATH_ARCHIVO_CONFIGURACION_TERMINAL,"r")
	x=archi.readline()
	direccion1=archi.readline()
	direccion2=archi.readline()
	return str(direccion2).replace('\n','')
