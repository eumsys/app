# -*- coding: utf-8 -*-
"""
Funciones para leer datos
"""
PATH_ARCHIVO_CONFIGURACION_TERMINAL="/home/pi/Documents/EUM_CONFIGURACION_EXP/ArchivosConfig/configuracionFechaHora.txt"
configuracion=[]

def getDatos():
	archivo=open(PATH_ARCHIVO_CONFIGURACION_TERMINAL, "r")
	for linea in archivo.readlines():
		configuracion.append(linea)
	archivo.close()
	pass

def getFecha():
	getDatos()
	return configuracion[0]
	pass

def getHora():
	getDatos()
	return configuracion[1]
	pass

#print getHora()

#print getNombre()
#print getEstado()
#print getMunicipio()
#print getTerminal()
