
import sys
import socket
import argparse
from datetime import datetime, date, time
import os


tam_buffer = 150



def descuentoAplicar(s,operacion,mensaje):
	#print("Bandera2")
	# operacion de registro de boleto desde la expedidora
	s.send(operacion.encode('utf-8'))
	# Espera una trama de confirmacion
	if (s.recv(tam_buffer) == b'ack'):
		# Realiza el envio de los datos del boleto a buscar
		s.send(mensaje.encode('utf-8'))
		data = s.recv(tam_buffer)
		if (data == b'Descuento aplicado'):
			print("Mensaje del servidor:",data)
			respuesta="Registro de \nDescuento Exitoso"
		else:
			print("Mensaje del servidor:",data)
			respuesta="Registro de \nDescuento Incorrecto"
	else:
		print("NO se entrego la operacion")
		respuesta="No se entrego la operacion"
	return respuesta

def inicioSesion(s,operacion,mensaje):
	# operacion de inicio de sesion
	s.send(operacion.encode('utf-8'))
	# Espera una trama de confirmacion
	if (s.recv(tam_buffer) == b'ack'):
		# Realiza el envio de los datos del boleto a buscar
		s.send(mensaje.encode('utf-8'))
		data = s.recv(tam_buffer)
		print(data)
		if (data != b'usuario y/o password incorrectas'):
			print("Incio de sesion exitoso")
			respuesta="Inicio de \nSesion Exitoso"
		else:
			print("Incio de sesion incorrecto:")
			respuesta="Usuario y/o constrasenias incorrectos"
			print(data)
	else:
		print("NO se entrego la operacion")
		respuesta="No se entrego la operacion"
	return respuesta



def menu():
	os.system('clear')
	print("Selecciona una opción")
	print("\t1 - Expedicion de Boleto")
	print("\t2 - Pago de Boleto")
	print("\t3 - Autorizacion de Salida")
	print("\t4 - Solicitud Descuento")
	print("\t5 - Descuento a aplicar")
	#print("\t9 - salir")



def configSocket(operacion,mensaje):
	#Parseo de argumentos, identifico que se tiene que pasar 2 parametros por consola host:127.0.0.1 puerto: 1234
	'''parser = argparse.ArgumentParser(description='Socket Error Examples')
	parser.add_argument('--host', action="store", dest="host", required=True)
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	given_args = parser.parse_args()
	host = given_args.host
	port = given_args.port'''
	host = "192.168.1.70"
	port = 2324

	# Bloque try - catch para crear el socket
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print("Error al crear el socket: {}".format(e))
		sys.exit(1)

	# Bloque try - catch para conectarse al servidor
	try:
		conn = s.connect((host,port))
		print("Conexion al host: {} en el puerto: {}".format(host,port))
		#print("--> conn {}".format(conn))
	except socket.gaierror as e:
		print("Error al conectar con el servidor: {}".format(e))
		sys.exit(1)
	except socket.error as e:
		print("Error de Conexion: {}".format(e))
		sys.exit(1)
	#print("Bandera1")    
	print(type(operacion))
	if(operacion=="descuento a aplicar"):
		print("Si entro")
		respuesta=descuentoAplicar(s,operacion,mensaje)
	elif(operacion=="inicio sesion"):
		respuesta=inicioSesion(s,operacion,mensaje)
		print("Si entro2")
	else:
		pass
	s.close()
	return respuesta
