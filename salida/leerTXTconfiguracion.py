# -*- coding: utf-8 -*-
"""
Funciones para leer datos
"""
PATH_ARCHIVO_CONFIGURACION_TERMINAL="/home/pi/Documents/EUM_CONFIGURACION_EXP/ArchivosConfig/configuracionTerminal.txt"
configuracion=[]

def getDatos():
	archivo=open(PATH_ARCHIVO_CONFIGURACION_TERMINAL, "r")
	for linea in archivo.readlines():
		configuracion.append(linea)
	archivo.close()
	pass

def getNombre():
	getDatos()
	return configuracion[0]
	pass

def getEstado():
	getDatos()
	return configuracion[1]
	pass

def getMunicipio():
	getDatos()
	return configuracion[2]
	pass

def getTerminal():
	getDatos()
	return configuracion[3]
	pass

#print getNombre()
#print getEstado()
#print getMunicipio()
#print getTerminal()
