# -*- coding: utf-8 -*-
"""
Estacionamientos unicos de México
GABRIEL MENDOZA RUIZ
Preguntar si a llegado al folio NUM_RESET_MAX_FOLIOS
"""

PATH_ARCHIVO_LEER_FOLIO="/home/pi/Documents/EUM_EXPE/Tickets/UltimoFolio.txt"
PATH_BITACORA_FOLIOS="/home/pi/Documents/EUM_EXPE/Tickets/foliosBitacoras.txt"
NUM_RESET_MAX_FOLIOS=10000

def setReset():
	archi = open(PATH_ARCHIVO_LEER_FOLIO,"r")
	numeroFol=archi.readline()
	archi.close()
	numeroFol=numeroFol.replace('\n','')
	if int(numeroFol)>=NUM_RESET_MAX_FOLIOS:		#Resetaremos el folio de 10000 a 0 para que emppiece la cuenta de folio de nuevo#De igual forma se pone un indicador en la bitacora
		archi = open(PATH_ARCHIVO_LEER_FOLIO,"w")
		archi.write('0'+'\n')
		archi2 = open(PATH_BITACORA_FOLIOS,"w")
		archi2.write('***********-----------------LLEGO AL FOLIO 10,000--------------------******************'+'\n')
		archi.close()
		archi2.close()
	#return numeroFol.replace('\n','')
#print setReset()
