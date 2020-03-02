from PyQt4 import QtCore, QtGui
import RPi.GPIO as GPIO
from registrosalida import Ui_Form
from threading import Thread
import scriptEntrada as sin

import os


def  main():
	os.system("lxterminal -e sudo python /home/pi/Desktop/Ticket/first.py   ")


def  main2():
	archivo= "1.mp4"
	os.system("omxplayer  --loop --win  \"500 0 1400 800\" /home/pi/Videos/admi/"+archivo+"")


#while(kill == 0)

if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	GPIO.setup(20,GPIO.IN)
	GPIO.setup(21,GPIO.IN)
	
	config1 = GPIO.input(20)
	config2 = GPIO.input(21)
	
	if(config1==True and config2==False):
		window = Ui_Form()
		sys.exit(app.exec_())
	elif(config2==True and config1==False):
		os.system("lxterminal -e sudo python /home/pi/Desktop/Ticket/first.py   ")
		
	elif(config1==True and config2==True):
		print("Acceso para programadores")
	elif(config1==False and config2==False):
		print("Acceso para Configurar")
		os.system("lxterminal -e sudo python /home/pi/ExpediraConfig/entrada.py  ")
	
	GPIO.cleanup()

