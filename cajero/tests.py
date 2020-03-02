# coding=utf-8
#!/usr/bin/env python3

'''
Version: CMB-1.3.1
Fecha: 26/12/2019

UPDATE:
- Scanner validacion directa.

INSTALACION :
- crear archivos: /home/cajero/Documentos/ticket.txt'
'''
import sys
import os
import time
import fechaUTC as hora
#import Conexiones.cliente as Servidor
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
from Pila.Pila import Pila
from Comunicacion import Comunicacion
from struct import *

#ruta = os.path.join(os.path.dirname(__file__))
#sys.path.append(ruta)
#ruta = ruta + "/"

from Variables.Variable import Variable
from Variables.Temporizador import Temporizador
from Monitor.Hopper import Hopper
from PuertoSerie import PuertoSerie
import traceback
from Logs.GuardarLogs import GuardarLogs



a = ["-","-","-","-","-"]



print(a)
a.pop(0)
a.append(33)

print(a)

a.pop(0)
a.append(245)

print(a)

a.pop(0)
a.append(244445)

print(a)

a.pop(0)
a.append(111)

print(a)

a.pop(0)
a.append(222)

print(a)

a.pop(0)
a.append(333)

print(a)

a.pop(0)
a.append(444)

print(a)