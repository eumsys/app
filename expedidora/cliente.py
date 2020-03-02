
import sys
import socket
import argparse
import datetime
import os

tam_buffer = 150

host = '192.168.1.129'
port = 2324

def registroBoleto(s,operacion):
	#operacion de registro de boleto desde la expedidora
	s.send(operacion.encode('utf-8'))
	# Espera una trama de confirmacion
	if(s.recv(tam_buffer) == b'ack'):
		#Realiza el envio de los datos del boleto a buscar
		resultado = "registro correcto"
	else:
		print("No se entrego la operacion")
		s.close()
		return "error"
	return s

def logExpedidora(s,operacion,mensaje):
	# operacion de inicio de sesion
	s.send(operacion.encode('utf-8'))
	# Espera una trama de confirmacion
	if (s.recv(tam_buffer) == b'ack'):
		# Realiza el envio de los datos del boleto a buscar
		s.send(mensaje.encode('utf-8'))
		data = s.recv(tam_buffer)
		print(data)
		if (data == b'log expedidora registrado'):
			print("Fin_log registrado")
		else:
			print("Error en registro log:")
			print(data)
	else:
		print("NO se entrego la operacion")
	s.close()

def enviarMensaje(s,mensaje):
	s.send(mensaje.encode('utf-8'))
	if(s.recv(tam_buffer) == b'registro exitoso del pago'):
		print("Registro Exitoso")
		resultado = "envio correcto"
	else:
		print("Registro Incorrecto")
		resultado = "error"
	s.close()
	return resultado

def configSocket(operacion):
	global host,port
	#Parseo de argumentos, identifico que se tiene que pasar 2 parametros por consola host:127.0.0.1 puerto: 1234
	'''parser = argparse.ArgumentParser(description='Socket Error Examples')
	parser.add_argument('--host', action="store", dest="host", required=True)
	parser.add_argument('--port', action="store", dest="port", type=int, required=True)
	given_args = parser.parse_args()
	host = given_args.host
	port = given_args.port'''
	# Bloque try - catch para crear el socket
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error as e:
		print("Error al crear el socket: {}".format(e))
		return "error"
		sys.exit(1)

	# Bloque try - catch para conectarse al servidor
	try:
		conn = s.connect((host,port))
		print("Conexion al host: {} en el puerto: {}".format(host,port))
		print("--> conn {}".format(conn))
	except socket.gaierror as e:
		print("Error al conectar con el servidor: {}".format(e))
		return "error"
		sys.exit(1)
	except socket.error as e:
		print("Error de Conexion: {}".format(e))
		return "error"
		sys.exit(1)
	if operacion != "log expedidora":
		validacion = registroBoleto(s,operacion)
		return validacion
	else:
		return s
