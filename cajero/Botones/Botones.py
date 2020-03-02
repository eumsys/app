# coding=utf-8
import sys
import threading
import serial
import time
import serial.tools.list_ports

sys.path.append("..")
from Variables import Variable


__author__ = "SIGFRIDO"
__date__ = "$20-may-2019 9:56:05$"


class Botones ():
	"""Clase utilizada comunicarse con un arduino y leer y escribir sus variables
	NumeroDeEntradasDigitales
	NumeroDeSalidasDigitales
	"""
	X=[]
	Y=[]
	
	PUERTO_ARDUINO = "USB2.0-Serial"
	PUERTO_ADAPTADOR = "USB-Serial Controller"
	PUERTO_ARDUINO_MICRO = "Arduino Micro"

	def __init__(self, nombreDelPuerto = "", entradasDigitales = 2, salidasDigitales = 2, **kwargs):
		
		puertoDeComunicacion = PuertoDeComunicacion("puerto")
		lista = puertoDeComunicacion.obtenerListaDeDispositivios()
		
		for key, value in kwargs.items(): 
			if key == "dispositivo":
				for elemento in lista:
					if value == elemento[2]:
						print ("El dispositivo es %s en el puerto %s" %(value, elemento[0]))
						nombreDelPuerto = elemento[0]
						break;

		self.__numeroDeEntradasDigitales = entradasDigitales
		self.__numeroDeSalidasDigitales = salidasDigitales

		self.crearVariables ()
		self.establecerPuerto(nombreDelPuerto)
		self.establecerEntradasDigitales()
		self.establecerSalidasDigitales()
			
			

		
		 
	def crearVariables (self):
		""""""
		for i in range (self.__numeroDeEntradasDigitales):
			self.X.append(Variable.Variable("", "", "", "", "", "", i))
			
		for i in range (self.__numeroDeSalidasDigitales):
			self.Y.append(Variable.Variable("", "", "", "", "", "", i))
			
	def establecerEntradaDigital(self, variable, indice):
		self.X[indice] = variable
		
	def obtenerEntradaDigital(self, indice):
		return self.X[indice]

	def establecerSalidaDigital (self, variable, indice):
		self.Y[indice] = variable
		
	def obtenerSalidaDigital (self, indice):
		return self.Y[indice]


	def establecerPuerto (self, NombreDelPuerto):
		try :
			self.__puerto = PuertoDeComunicacion (NombreDelPuerto)
			self.__puerto.start()
			#print ("Iniciar")

			self.__puerto.abrirPuerto(NombreDelPuerto, 9600)
			#print ("Despues de abrir el  puerto >>", self.__puerto.estado)
			time.sleep(2)
			self.__puerto.escribir('-')

		except:
			print ("No se pudo establecer el puerto de comunicacion->Establecer puerto")
			
			
	def cerrarPuerto(self):
		self.__puerto.cerrarPuerto()
		
	def establecerEntradasDigitales (self):
		self.__puerto.establecerProtocolo_01(self.funcion)
		print ("Se establecio el protocolo")
		
	def establecerSalidasDigitales (self):
		for i in range (self.__numeroDeSalidasDigitales):
			self.Y[i].establecerInterfaz(self.funcion01)
		
	def funcion (self, dato):

		self.X[0].establecerValor(int (dato)& 1)
		self.X[1].establecerValor((int (dato))>>1 & 1 )
		self.X[2].establecerValor((int (dato))>>2 & 1 )
		
	def funcionEnviar (self, indice, dato):
		return (chr(ord('a')+indice+ (ord('A')-ord('a'))*dato))
		
	def funcion01 (self, indice, dato):
		self.__puerto.escribir(self.funcionEnviar(indice, dato))
		

class PuertoDeComunicacion (threading.Thread):
	

	

	def __init__ (self, nombre):
		threading.Thread.__init__ (self, name = nombre)

		self.estado = False
		self.auxiliar = self.estado
		self.funcionando = False;

		self.__puertoSerie = serial.Serial()

			 
	def abrirPuerto (self, puerto, baud):
		self.__puertoSerie.port = (puerto)
		self.__puertoSerie.baudrate = baud
		self.__puertoSerie.parity = serial.PARITY_SPACE
		self.__puertoSerie.timeout = 0
		self.__puertoSerie.stopbits = serial.STOPBITS_ONE
		self.__puertoSerie.bytesize = serial.EIGHTBITS

		self.estado = True
		print ("Se abrio el puerto")


	def cerrarPuerto (self):
		self.estado = False
		self.funcionando = False
		#print ("self.estado ", self.estado)
		#print ("self.auxiliar ", self.auxiliar)

		
	def leer (self):
		if self.__puertoSerie.is_open:
			self.__puertoSerie.flush()
			s = self.__puertoSerie.read(1)

			#print ("Leyendo")
			if s:
				#print ("RECIBIDO >>", s)

				try:
					self.__protocolo_01(s)
				except:
					""""""
					#print ("El protocolo no existe")


	def escribir (self, mensaje):
		#print (self.__puertoSerie.is_open)
		
		try:
			self.__puertoSerie.write(mensaje.encode ('UTF-8'))
			#print ("Escribiendo %s" % (mensaje))
			
		except:
			print ("No se pudo escribir")

		
	def obtenerListaDePuertos (self) :
		ports = list(serial.tools.list_ports.comports()) 
		cTupla =()
		for port in ports:
			print (port.device)
			cTupla  += port.device,
		#print (cTupla)
		return (cTupla)


	def obtenerListaDeDispositivios (self) :
		ports = list(serial.tools.list_ports.comports()) 
		cTupla =()
		
		for port in ports:
			dTupla = ()
			"""
			cLista = []
			cLista.append (port.device)
			cLista.append (port.name)
			cLista.append (port.description)
			"""
			
			dTupla += port.device,
			dTupla += port.name,
			dTupla += port.description,
			"""
			print ("\n")

			print ("device: ", port.device)
			print ("name: ", port.name)
			print ("description: ", port.description)
			print ("hwid: ", port.hwid)
			print ("hwid: ", port.vid)
			print ("pid: ", port.pid)
			print ("serial_number: ", port.serial_number)
			print ("location: ", port.location)
			print ("manufacturer: ", port.manufacturer)
			print ("product: ", port.product)
			print ("interface: ", port.interface)
			"""

			#cTupla  += port.device,
			cTupla  += dTupla,
		#print (cTupla)
		return (cTupla)


	#def establecerInterfaz (self, interfaz):
	#    self.interfaz = interfaz

	#def establecerProtocolo (protocolo):
	#    self.__protocolo = protocolo

	def establecerProtocolo_01(self, protocolo_01):
		self.__protocolo_01 = protocolo_01
		
		
	def run (self):
		self.estado = False
		self.auxiliar = self.estado
		self.funcionando = True
		
		while self.funcionando :

			if self.estado :
								
				if self.auxiliar == False:
					"""Abrir puerto"""
					try:
						self.__puertoSerie.open()
					except serial.serialutil.SerialException as serialException:
						print ("Excepcion \n%s" % serialException)
						#self.interfaz.escribirMensajero1("\nNo se pudo abrir el puerto \n%s" % serialException)
						self.estado = False

					if self.__puertoSerie.is_open:
						#self.interfaz.escribirMensajero1("\nPuerto %s a %d %s abierto " % (self.__puertoSerie.port, self.__puertoSerie.baudrate, self.__puertoSerie.parity))
						self.auxiliar = True
						
				self.leer()
	#                self.escribir("prueba")
			else:
				"""cerrar Puerto"""
				if (self.__puertoSerie.is_open):
					self.__puertoSerie.close()
					#self.interfaz.escribirMensajero1("\nPuerto %s cerrado " % self.__puertoSerie.port)
					self.auxiliar = self.estado
					
			#time.sleep (0.001)
					
		print ("Hilo terminado")
		

def obtenerNombreDelPuerto (**kwargs):
	puertoDeComunicacion = PuertoDeComunicacion("puerto")
	lista = puertoDeComunicacion.obtenerListaDeDispositivios()
	nombreDelPuerto=""
	
	for key, value in kwargs.items(): 
		if key == "dispositivo":
			for elemento in lista:
				if value == elemento[2]:
					print ("El dispositivo es %s en el puerto %s" %(value, elemento[0]))
					nombreDelPuerto = elemento[0]
					break;
					
	return nombreDelPuerto


def main ():
	#Se crea el constructor e inicia el puerto de comunicación
	#Botones("/dev/ttyUSB0", 3, 2)
	botones = Botones("COM6", 3, 2)


	#Ejemplo de Lectura

	while True:
		a = botones.X[0].obtenerValor()
		b = botones.X[1].obtenerValor()
		c = botones.X[2].obtenerValor()
		print (a, b, c)
		time.sleep (0.1)
	"""

	#Ejemplo de escritura

	time.sleep(4)
	botones.Y[0].establecerValor(1)
	time.sleep(2)
	botones.Y[1].establecerValor(1)

	time.sleep(2)
	botones.Y[0].establecerValor(0)
	time.sleep(2)
	botones.Y[1].establecerValor(0)

	"""

	#Para cerrar el puerto de comunicación
	botones.cerrarPuerto()

if __name__ == "__main__":
    main()
