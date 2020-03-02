from PyQt4 import QtCore, QtGui
import RPi.GPIO as GPIO
from registrosalida import Ui_Form
from threading import Thread

import time,os
import commands
from threading import Thread
import os
PATH_PONER_DATOS_TICKET="/home/pi/Documents/CAJA_1_Monterrey/datos_tikets/ticket.txt "
PATH_PONER_DATOS_TICKET_AUX="/home/pi/Documents/CAJA_1_Monterrey/datos_tikets/ticketAux.txt"
DESPLEGAR_CAMARA="sudo zbarcam --raw  --prescale=10x10"
DESPLEGAR_INTERFAZ_ENTRADA="sudo python /home/pi/Documents/CAJA_1_Monterrey/registrosalida.py"

def activarCamara():
	print "EL hilo ...." 
	os.system("rm "+PATH_PONER_DATOS_TICKET)
	os.system("rm "+PATH_PONER_DATOS_TICKET_AUX)
	os.system(DESPLEGAR_CAMARA+" >> "+PATH_PONER_DATOS_TICKET)
	os.system(" echo -1 >> "+PATH_PONER_DATOS_TICKET)
	os.system(" echo [Error] Camara >> "+PATH_PONER_DATOS_TICKET)
	os.system(" echo [Error] Devolvio un estado de ERROR  ...>> "+PATH_PONER_DATOS_TICKET)
	os.system(" echo [Error] Asegurate de conectar la camara. >> "+PATH_PONER_DATOS_TICKET)

def ejecutaInterfaz():
	os.system(DESPLEGAR_INTERFAZ_ENTRADA)

def Hilos():
	thread1 = Thread(target = activarCamara, args=())
	thread2 = Thread(target = ejecutaInterfaz, args=())
	try:
		thread1.start()
		thread2.start()
	except Exception:
		pass
		
	while(thread1.is_alive):
		kill = 0
	kill = 1



if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	os.system("lxterminal -e sudo python3 /home/pi/Documents/cajero/cajero.py")

