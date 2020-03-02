# -*- coding: utf-8 -*-
"""
Estacionamientos unicos de México
Este archivo es para remplaar a acceso4.py
Funcion: 		Funcion de codigoQR
Descripcion:	 genera codigo qr para imprimir 
Funciones que se pueden usar:
	1) generarCodigo
	2) construirCodigo
	3) construirCodigoEntrada()
Formato de codigo:
	folio
	terminal de entrada
	fecha de entrada
	hora de entrada
"""
import pyqrcode

PATH_CODIGOS_QR="/home/pi/Documents/EUM_EXPE/CodigosQR/outputQR.png"


def construirCodigoEntrada(nb,te,fe,he):
	cadena="Estacionamientos unicos de Mexico\n"+str(nb)+"\n"+str(te)+"\n"+fe+"\n"+he
	codqr = pyqrcode.create(str(cadena))
	codqr.png(PATH_CODIGOS_QR, scale=6)
	return True
	pass	
