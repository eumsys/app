#!/usr/bin/env python3
import sys
import os
import time
import fechaUTC as hora
import Conexiones.cliente as Servidor
#from pygame import mixer
import subprocess
#import imprimirBoleto as impresora
from threading import Timer,Thread 
import sched
import termios
import serial
import binascii
from bitstring import BitArray
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog, QGridLayout, QMessageBox,QLabel, QPushButton, QLineEdit,QSpinBox, QTableWidget,QTableWidgetItem,QComboBox,QCheckBox
from PyQt5 import QtCore, QtGui, uic
from datetime import datetime, timedelta
import calendar
import psycopg2, psycopg2.extras
from Botones.Botones import Botones,PuertoDeComunicacion, obtenerNombreDelPuerto
from Conexiones.Conexiones import Conexiones
from Pila.Pila import Pila

from Comunicacion import Comunicacion
from struct import *


ruta = os.path.join(os.path.dirname(__file__))
sys.path.append(ruta)

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador
from Monitor.Hopper import Hopper

contador = 0
ct_max = 5

INSTRUCCIONES = ["A_MON","A_BIL","CAMBIO","CHECK_SENSOR"]

TON_01 = Temporizador("TON_01",2/ct_max)
while(True):
	TON_01.entrada = not TON_01.salida
	TON_01.actualizar()
	if TON_01.salida:
		contador+=1

		print("req ----- ",contador)
		if( contador >= ct_max):
			contador = 0 

		if contador == 0:
			print("acamero ----- ",contador)
			time.sleep(1)
		if contador == 1:
			print("acamero ----- ",contador)
		if contador == 2:
			print("acamero ----- ",contador)
		if contador == 3:
			print("acamero ----- ",contador)
		if contador == 4:
			print("acamero ----- ",contador)

		print("contador: ",contador)

